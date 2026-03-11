const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL?.trim().replace(/\/$/, "") ?? ""
const mockFlag = process.env.NEXT_PUBLIC_USE_MOCK_API

export const appEnv = {
  apiBaseUrl,
  useMockApi: mockFlag ? mockFlag === "true" : apiBaseUrl.length === 0,
}

