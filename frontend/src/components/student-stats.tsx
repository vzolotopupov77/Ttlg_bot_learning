import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import type { StudentStatsRead } from "@/lib/types/students"

type StudentStatsProps = {
  stats: StudentStatsRead
}

export function StudentStats({ stats }: StudentStatsProps) {
  const hwPercent =
    stats.assignments_total > 0
      ? Math.round(
          (100 * stats.assignments_done) / stats.assignments_total,
        )
      : 0

  return (
    <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
      <Card className="gap-0 py-0">
        <CardHeader className="pb-2">
          <CardTitle className="text-muted-foreground text-sm font-medium">
            Всего занятий
          </CardTitle>
        </CardHeader>
        <CardContent className="pt-0">
          <p className="text-2xl font-semibold">{stats.lessons_total}</p>
        </CardContent>
      </Card>

      <Card className="gap-0 py-0">
        <CardHeader className="pb-2">
          <CardTitle className="text-muted-foreground text-sm font-medium">
            Завершено занятий
          </CardTitle>
        </CardHeader>
        <CardContent className="pt-0">
          <p className="text-2xl font-semibold">{stats.lessons_completed}</p>
          <p className="text-muted-foreground mt-1 text-xs">
            из {stats.lessons_total}
          </p>
        </CardContent>
      </Card>

      <Card className="gap-0 py-0">
        <CardHeader className="pb-2">
          <CardTitle className="text-muted-foreground text-sm font-medium">
            Выполнение ДЗ
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 pt-0">
          <p
            className={cn(
              "text-2xl font-semibold",
              hwPercent >= 70 && "text-success",
            )}
          >
            {stats.assignments_total === 0 ? "—" : `${hwPercent}%`}
          </p>
          <div className="bg-muted h-2 w-full overflow-hidden rounded-full">
            <div
              className="bg-primary h-full rounded-full transition-[width]"
              style={{
                width:
                  stats.assignments_total === 0
                    ? "0%"
                    : `${hwPercent}%`,
              }}
            />
          </div>
          <p className="text-muted-foreground text-xs">
            {stats.assignments_total === 0
              ? "Нет назначенных ДЗ"
              : `${stats.assignments_done} из ${stats.assignments_total}`}
          </p>
        </CardContent>
      </Card>

      <Card className="gap-0 py-0">
        <CardHeader className="pb-2">
          <CardTitle className="text-muted-foreground text-sm font-medium">
            Проверено
          </CardTitle>
        </CardHeader>
        <CardContent className="pt-0">
          <p className="text-2xl font-semibold">
            {stats.lessons_solution_checked}
          </p>
          <p className="text-muted-foreground mt-1 text-xs">
            Занятия с проверенным решением
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
