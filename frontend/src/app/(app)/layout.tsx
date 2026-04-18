import type { Metadata } from "next"
import { redirect } from "next/navigation"

import { Header } from "@/components/header"
import { Sidebar } from "@/components/sidebar"
import { getUser } from "@/lib/auth"

export const metadata: Metadata = {
  title: "Репетитор",
  description: "Система управления занятиями",
}

export default async function AppLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  const user = await getUser()
  if (!user) {
    redirect("/login")
  }

  return (
    <div className="flex min-h-0 flex-1">
      <Sidebar user={user} />
      <div className="flex min-h-0 min-w-0 flex-1 flex-col">
        <Header user={user} />
        <main className="flex-1 overflow-auto p-4">{children}</main>
      </div>
    </div>
  )
}
