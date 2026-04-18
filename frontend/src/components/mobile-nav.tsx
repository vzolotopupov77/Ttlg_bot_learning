"use client"

import { BookOpen, Calendar, Menu, Settings, Users } from "lucide-react"
import { useState } from "react"

import { NavLink } from "@/components/nav-link"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import {
  Sheet,
  SheetContent,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import type { UserPublic } from "@/lib/auth"

type MobileNavProps = {
  user: UserPublic
}

export function MobileNav({ user }: MobileNavProps) {
  const [open, setOpen] = useState(false)

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger
        render={
          <Button
            type="button"
            variant="ghost"
            size="icon"
            className="md:hidden"
            aria-label="Открыть меню"
          >
            <Menu className="size-5" />
          </Button>
        }
      />
      <SheetContent side="left" className="w-72 bg-sidebar p-0 text-sidebar-foreground">
        <SheetTitle className="sr-only">Навигация</SheetTitle>
        <div className="flex flex-col gap-4 p-4">
          <div className="flex items-center gap-2 font-semibold">
            <BookOpen className="size-6 text-sidebar-primary" />
            <span>Репетитор</span>
          </div>
          <Separator />
          <nav
            className="flex flex-col gap-1"
            onClick={() => setOpen(false)}
          >
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
              <NavLink
                href="/student/schedule"
                icon={<Calendar className="size-4" />}
              >
                Моё расписание
              </NavLink>
            )}
          </nav>
        </div>
      </SheetContent>
    </Sheet>
  )
}
