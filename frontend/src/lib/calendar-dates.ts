import { addDays, format, isValid, parseISO, startOfWeek } from "date-fns"
import { ru } from "date-fns/locale"

export function mondayOfDate(d: Date): Date {
  return startOfWeek(d, { weekStartsOn: 1 })
}

export function mondayThisWeek(): string {
  return format(mondayOfDate(new Date()), "yyyy-MM-dd")
}

export function parseWeekStart(param?: string | null): string {
  if (!param) {
    return mondayThisWeek()
  }
  const d = parseISO(param)
  if (!isValid(d)) {
    return mondayThisWeek()
  }
  return format(mondayOfDate(d), "yyyy-MM-dd")
}

export function weekDaysFromMonday(weekStart: string): {
  date: Date
  key: string
  weekdayShort: string
  dayNum: string
}[] {
  const monday = parseISO(weekStart)
  return Array.from({ length: 7 }, (_, i) => {
    const d = addDays(monday, i)
    return {
      date: d,
      key: format(d, "yyyy-MM-dd"),
      weekdayShort: format(d, "EEE", { locale: ru }),
      dayNum: format(d, "d"),
    }
  })
}

export function addWeeksToMonday(weekStart: string, deltaWeeks: number): string {
  const monday = parseISO(weekStart)
  const next = addDays(monday, deltaWeeks * 7)
  return format(mondayOfDate(next), "yyyy-MM-dd")
}

export function formatWeekRangeLabel(weekStart: string): string {
  const monday = parseISO(weekStart)
  const sunday = addDays(monday, 6)
  return `${format(monday, "d.MM")} — ${format(sunday, "d.MM.yyyy", { locale: ru })}`
}

export function isTodayKey(dayKey: string): boolean {
  const today = format(new Date(), "yyyy-MM-dd")
  return dayKey === today
}
