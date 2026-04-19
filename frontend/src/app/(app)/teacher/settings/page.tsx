import { SettingsForm } from "@/components/settings-form"
import { fetchSettings } from "@/lib/api-server"
import type { SystemSettings } from "@/lib/types/settings"

function settingsFormKey(data: SystemSettings) {
  return [
    data.teacher_name,
    data.default_lesson_duration_minutes,
    data.lesson_reminder_hours_before,
    data.homework_reminder_hours_before,
  ].join("|")
}

export default async function TeacherSettingsPage() {
  const initialData = await fetchSettings()

  return (
    <div className="flex flex-col gap-4">
      <div>
        <h1 className="font-heading text-xl font-semibold">Настройки системы</h1>
        <p className="text-sm text-muted-foreground">
          Параметры преподавателя и напоминаний для учеников
        </p>
      </div>
      <SettingsForm
        key={settingsFormKey(initialData)}
        initialData={initialData}
      />
    </div>
  )
}
