export default function AuthLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <div className="min-h-svh bg-gradient-to-b from-muted/50 via-background to-background">
      {children}
    </div>
  )
}

