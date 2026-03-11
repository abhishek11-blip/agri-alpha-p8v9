"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"

import { queryKeys } from "@/lib/query-keys"
import {
  createAdminPassType,
  deleteAdminPassType,
  getAdminPassTypes,
  getDashboardStats,
  updateAdminPassType,
} from "@/services/admin.service"
import { getMyPasses, getPassTypes, purchasePass } from "@/services/pass.service"
import { getTripHistory } from "@/services/trip.service"
import { validatePass } from "@/services/validator.service"
import type { TripHistoryFilters } from "@/types/trip"
import type { UpsertPassTypeInput } from "@/types/admin"

export function usePassTypesQuery(enabled = true) {
  return useQuery({
    queryKey: queryKeys.passTypes,
    queryFn: getPassTypes,
    enabled,
  })
}

export function useMyPassesQuery(enabled = true) {
  return useQuery({
    queryKey: queryKeys.myPasses,
    queryFn: getMyPasses,
    enabled,
  })
}

export function usePurchasePassMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: purchasePass,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.myPasses })
      queryClient.invalidateQueries({ queryKey: queryKeys.adminDashboard })
    },
  })
}

export function useTripHistoryQuery(filters: TripHistoryFilters, enabled = true) {
  return useQuery({
    queryKey: queryKeys.tripsHistory(filters),
    queryFn: () => getTripHistory(filters),
    enabled,
  })
}

export function useValidatePassMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: validatePass,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["trips", "history"] })
      queryClient.invalidateQueries({ queryKey: queryKeys.adminDashboard })
    },
  })
}

export function useAdminDashboardQuery(enabled = true) {
  return useQuery({
    queryKey: queryKeys.adminDashboard,
    queryFn: getDashboardStats,
    enabled,
  })
}

export function useAdminPassTypesQuery(enabled = true) {
  return useQuery({
    queryKey: queryKeys.adminPassTypes,
    queryFn: getAdminPassTypes,
    enabled,
  })
}

export function useCreateAdminPassTypeMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (input: UpsertPassTypeInput) => createAdminPassType(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.adminPassTypes })
      queryClient.invalidateQueries({ queryKey: queryKeys.passTypes })
    },
  })
}

export function useUpdateAdminPassTypeMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: { passTypeId: string; input: UpsertPassTypeInput }) =>
      updateAdminPassType(payload.passTypeId, payload.input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.adminPassTypes })
      queryClient.invalidateQueries({ queryKey: queryKeys.passTypes })
    },
  })
}

export function useDeleteAdminPassTypeMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (passTypeId: string) => deleteAdminPassType(passTypeId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.adminPassTypes })
      queryClient.invalidateQueries({ queryKey: queryKeys.passTypes })
    },
  })
}

