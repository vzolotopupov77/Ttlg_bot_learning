import { BookOpen, Calendar, Settings, Users } from "lucide-react"

import { NavLink } from "@/components/nav-link"
import { Separator } from "@/components/ui/separator"
import type { UserPublic } from "@/lib/auth"

type SidebarProps = {
  user: UserPublic
}

export function Sidebar({ user }: SidebarProps) {
  return (
    <aside className="hidden h-full w-64 shrink-0 flex-col border-r border-sidebar-border bg-sidebar text-sidebar-foreground md:flex">
      <div className="flex flex-col gap-4 p-4">
        <div className="flex items-center gap-2 font-semibold">
          <BookOpen className="size-6 text-sidebar-primary" />
          <span>Репетитор</span>
        </div>
        <Separator />
        <nav className="flex flex-col gap-1">
          {user.role === "teacher" ? (
            <>
              <NavLink
                href="/teacher/calendar"
                icon={<Calendar className="size-4" />}
              >
                Календарь
              </NavLink>
              <NavLink href="/teacher/students" icon={<Users className="size-4" />}>
                Ученики
              </NavLink>
              <NavLink
                href="/teacher/settings"
                icon={<Settings className="size-4" />}
              >
                Настройки
              </NavLink>
            </>
          ) : (
            <NavLink href="/student/schedule" icon={<Calendar className="size-4" />}>
              Моё расписание
            </NavLink>
          )}
        </nav>
      </div>
    </aside>
  )
}
