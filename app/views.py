from datetime import timedelta

import uuid

from django.utils import timezone
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from rest_framework.generics import ListAPIView

from .models import PassType, UserPass, Trip, TransportMode
from .serializers import RegisterSerializer, PassTypeSerializer, TripSerializer
from rest_framework.permissions import IsAdminUser


class RegisterView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PassTypesView(ListAPIView):

    permission_classes = [permissions.IsAuthenticated]

    queryset = PassType.objects.prefetch_related("transport_modes").all()

    serializer_class = PassTypeSerializer


class PurchasePassView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        pass_type_id = request.data.get("pass_type")

        if not pass_type_id:
            return Response(
                {"error": "pass_type is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            pass_type = PassType.objects.get(id=pass_type_id)
        except PassType.DoesNotExist:
            return Response(
                {"error": "Invalid pass type"}, status=status.HTTP_404_NOT_FOUND
            )

        expiry = timezone.now() + timedelta(days=pass_type.validity_days)

        user_pass = UserPass.objects.create(
            user=request.user,
            pass_type=pass_type,
            pass_code=str(uuid.uuid4()),
            expiry_date=expiry,
            status="ACTIVE",
        )

        return Response(
            {
                "message": "Pass purchased successfully",
                "pass_code": user_pass.pass_code,
                "expiry_date": expiry,
            },
            status=status.HTTP_201_CREATED,
        )


class ValidatePass(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        if request.user.role != "VALIDATOR":
            return Response(
                {"error": "Only validators can validate passes"},
                status=status.HTTP_403_FORBIDDEN,
            )

        pass_code = request.data.get("pass_code")
        transport_mode_id = request.data.get("transport_mode")

        if not pass_code or not transport_mode_id:
            return Response(
                {"error": "pass_code and transport_mode are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_pass = UserPass.objects.select_related("pass_type").get(
                pass_code=pass_code
            )
        except UserPass.DoesNotExist:
            return Response(
                {"error": "Invalid pass code"}, status=status.HTTP_404_NOT_FOUND
            )

        # Expiry Check
        if user_pass.expiry_date < timezone.now():
            user_pass.status = "EXPIRED"
            user_pass.save()

            return Response(
                {"error": "Pass expired"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            transport_mode = TransportMode.objects.get(id=transport_mode_id)
        except TransportMode.DoesNotExist:
            return Response(
                {"error": "Invalid transport mode"}, status=status.HTTP_404_NOT_FOUND
            )

        # Transport Mode Check
        if not user_pass.pass_type.transport_modes.filter(
            id=transport_mode.id
        ).exists():
            return Response(
                {"error": "Transport mode not covered"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Anti Passback Check (5 minutes)
        last_trip = (
            Trip.objects.filter(user_pass=user_pass).order_by("-validated_at").first()
        )

        if last_trip:
            diff = timezone.now() - last_trip.validated_at
            if diff < timedelta(minutes=5):
                return Response(
                    {"error": "Please wait before next validation"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Daily Trip Limit
        today = timezone.now().date()

        today_trips = Trip.objects.filter(
            user_pass=user_pass, validated_at__date=today
        ).count()

        max_trips = user_pass.pass_type.max_trips_per_day

        if max_trips and today_trips >= max_trips:
            return Response(
                {"error": "Daily trip limit reached"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create Trip
        Trip.objects.create(
            user_pass=user_pass,
            validated_by=request.user,
            transport_mode=transport_mode,
        )

        return Response(
            {"message": "Pass validated successfully"}, status=status.HTTP_200_OK
        )


class TripHistory(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        trips = Trip.objects.filter(user_pass__user=request.user)

        if start_date and end_date:
            trips = trips.filter(validated_at__date__range=[start_date, end_date])

        serializer = TripSerializer(trips, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminDashboard(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        if request.user.role != "ADMIN":
            return Response(
                {"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN
            )

        total_passes = UserPass.objects.count()

        total_trips = Trip.objects.count()

        mode_stats = Trip.objects.values("transport_mode__name").annotate(
            total=Count("id")
        )

        return Response(
            {
                "total_passes_sold": total_passes,
                "total_validations": total_trips,
                "validations_by_mode": mode_stats,
            }
        )


class CreateTransportMode(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request):

        name = request.data.get("name")

        if not name:
            return Response(
                {"error": "Transport mode name required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        name = name.strip()

        # duplicate check (case insensitive)
        if TransportMode.objects.filter(name__iexact=name).exists():
            return Response(
                {"error": "Transport mode already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        transport = TransportMode.objects.create(name=name)

        return Response(
            {
                "message": "Transport mode created successfully",
                "id": transport.id,
                "name": transport.name,
            },
            status=status.HTTP_201_CREATED,
        )


class CreatePassType(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request):

        name = request.data.get("name")
        price = request.data.get("price")
        validity_days = request.data.get("validity_days")
        daily_trip_limit = request.data.get("daily_trip_limit")
        transport_modes = request.data.get("transport_modes", [])

        pass_type = PassType.objects.create(
            name=name,
            price=price,
            validity_days=validity_days,
            daily_trip_limit=daily_trip_limit,
        )

        pass_type.transport_modes.set(transport_modes)

        return Response({"message": "Pass type created", "pass_type_id": pass_type.id})
