"use client"

import dynamic from "next/dynamic"
import { usePathname } from "next/navigation"

import { LogoutButton } from "@/components/logout-button"
import { ThemeToggle } from "@/components/theme-toggle"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import type { UserPublic } from "@/lib/auth"

const MobileNav = dynamic(
  () =>
    import("@/components/mobile-nav").then((m) => ({ default: m.MobileNav })),
  { ssr: false },
)

const ROUTE_TITLES: Array<{ prefix: string; title: string }> = [
  { prefix: "/teacher/calendar", title: "Календарь" },
  { prefix: "/teacher/students", title: "Ученики" },
  { prefix: "/teacher/settings", title: "Настройки" },
  { prefix: "/student/schedule", title: "Расписание" },
]

function titleForPath(pathname: string): string {
  const row = ROUTE_TITLES.find(
    (r) => pathname === r.prefix || pathname.startsWith(`${r.prefix}/`),
  )
  return row?.title ?? "Репетитор"
}

type HeaderProps = {
  user: UserPublic
}

export function Header({ user }: HeaderProps) {
  const pathname = usePathname()
  const title = titleForPath(pathname)

  return (
    <header className="flex h-14 shrink-0 items-center justify-between gap-4 border-b border-border px-4">
      <div className="flex min-w-0 items-center gap-3">
        <MobileNav user={user} />
        <h1 className="truncate text-lg font-semibold">{title}</h1>
      </div>
      <div className="flex items-center gap-2">
        <ThemeToggle />
        <Avatar className="size-9">
          <AvatarFallback>{user.name.slice(0, 2).toUpperCase()}</AvatarFallback>
        </Avatar>
        <LogoutButton />
      </div>
    </header>
  )
}
