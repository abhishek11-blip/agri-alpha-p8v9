"use client"

import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"
import { BarChart3Icon, CheckCircle2Icon, ClockIcon, TicketIcon } from "lucide-react"

import { ProtectedRoute } from "@/components/auth/protected-route"
import { PageHeader } from "@/components/common/page-header"
import { StatCard } from "@/components/common/stat-card"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart"
import { Spinner } from "@/components/ui/spinner"
import { useAdminDashboardQuery } from "@/hooks/use-maas-api"
import { TRANSPORT_MODE_LABELS } from "@/lib/constants"

const chartConfig = {
  count: {
    label: "Validations",
    color: "var(--chart-2)",
  },
} satisfies ChartConfig

export default function AdminDashboardPage() {
  const dashboardQuery = useAdminDashboardQuery(true)

  if (dashboardQuery.isLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <Spinner className="size-5" />
      </div>
    )
  }

  const stats = dashboardQuery.data

  return (
    <ProtectedRoute allowedRoles={["ADMIN"]}>
      <div className="space-y-5">
        <PageHeader
          title="Admin Analytics"
          description="Sales and validations overview for the transit pass system."
        />

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <StatCard
            title="Passes Sold Today"
            value={stats?.passesSold.daily ?? 0}
            icon={TicketIcon}
          />
          <StatCard
            title="Passes Sold Weekly"
            value={stats?.passesSold.weekly ?? 0}
            icon={ClockIcon}
          />
          <StatCard
            title="Active Passes"
            value={stats?.activePasses ?? 0}
            icon={CheckCircle2Icon}
          />
          <StatCard
            title="Expired Passes"
            value={stats?.expiredPasses ?? 0}
            icon={BarChart3Icon}
          />
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Validations by Transport Mode</CardTitle>
          </CardHeader>
          <CardContent>
            <ChartContainer config={chartConfig} className="h-72 w-full">
              <BarChart
                data={(stats?.validationsByMode ?? []).map((entry) => ({
                  mode: TRANSPORT_MODE_LABELS[entry.mode],
                  count: entry.count,
                }))}
              >
                <CartesianGrid vertical={false} />
                <XAxis
                  dataKey="mode"
                  tickLine={false}
                  tickMargin={8}
                  axisLine={false}
                />
                <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
                <Bar dataKey="count" fill="var(--color-count)" radius={8} />
              </BarChart>
            </ChartContainer>
          </CardContent>
        </Card>
      </div>
    </ProtectedRoute>
  )
}

