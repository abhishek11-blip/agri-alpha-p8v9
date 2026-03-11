# from rest_framework import serializers
# from .models import *
# from django.contrib.auth.hashers import make_password


# class RegisterSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ["username", "email", "mobile", "password", "role"]

#     def create(self, validated_data):

#         validated_data["password"] = make_password(validated_data["password"])

#         return super().create(validated_data)


# class PassTypeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = PassType
#         fields = "__all__"


# class UserPassSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = UserPass
#         fields = "__all__"


# class TripSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Trip
#         fields = "__all__"


from rest_framework import serializers
from .models import User, PassType, UserPass, Trip, TransportMode
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "mobile", "password", "role"]

    def create(self, validated_data):

        validated_data["password"] = make_password(validated_data["password"])

        return super().create(validated_data)


class PassTypeSerializer(serializers.ModelSerializer):

    transport_modes = serializers.StringRelatedField(many=True)

    class Meta:
        model = PassType
        fields = "__all__"


class TripSerializer(serializers.ModelSerializer):

    transport_mode = serializers.StringRelatedField()

    class Meta:
        model = Trip
        fields = ["id", "transport_mode", "route_info", "validated_at"]
