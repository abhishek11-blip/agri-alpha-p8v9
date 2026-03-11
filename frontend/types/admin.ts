import type { PassType, TransportModeCode } from "@/types/pass"

export interface DashboardStats {
  passesSold: {
    daily: number
    weekly: number
    monthly: number
  }
  validationsByMode: Array<{
    mode: TransportModeCode
    count: number
  }>
  activePasses: number
  expiredPasses: number
}

export interface UpsertPassTypeInput {
  name: string
  validityDays: number
  price: number
  transportModes: TransportModeCode[]
  maxTripsPerDay: number | null
}

export interface PassTypeMutationResponse {
  passType: PassType
}

export interface AdminPassTypesResponse {
  passTypes: PassType[]
}

