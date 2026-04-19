"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { Save } from "lucide-react"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { toast } from "sonner"
import { z } from "zod"

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Field,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Spinner } from "@/components/ui/spinner"
import { updateSettingsAction } from "@/app/actions/settings"
import type { SystemSettings } from "@/lib/types/settings"

/** Совпадает с `SettingsBody` в backend (`api/settings.py`). */
const settingsFormSchema = z.object({
  teacher_name: z.string().min(1, "Укажите имя репетитора"),
  default_lesson_duration_minutes: z
    .number({ error: () => ({ message: "Укажите число от 15 до 240" }) })
    .min(15, "Минимум 15 минут")
    .max(240, "Максимум 240 минут"),
  lesson_reminder_hours_before: z
    .number({ error: () => ({ message: "Укажите число от 1 до 168" }) })
    .min(1, "Минимум 1 час")
    .max(168, "Максимум 168 часов"),
  homework_reminder_hours_before: z
    .number({ error: () => ({ message: "Укажите число от 1 до 336" }) })
    .min(1, "Минимум 1 час")
    .max(336, "Максимум 336 часов"),
})

type SettingsFormValues = z.infer<typeof settingsFormSchema>

type SettingsFormProps = {
  initialData: SystemSettings
}

export function SettingsForm({ initialData }: SettingsFormProps) {
  const [baseline, setBaseline] = useState<SystemSettings>(initialData)

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<SettingsFormValues>({
    resolver: zodResolver(settingsFormSchema),
    defaultValues: initialData,
  })

  const onReset = () => {
    reset(baseline)
  }

  const onSubmit = async (data: SettingsFormValues) => {
    const result = await updateSettingsAction(data)
    if (result.ok) {
      setBaseline(result.settings)
      reset(result.settings)
      toast.success("Настройки сохранены")
    } else {
      toast.error(result.error)
    }
  }

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="flex max-w-2xl flex-col gap-6"
      noValidate
    >
      <Card>
        <CardHeader>
          <CardTitle>Общие настройки</CardTitle>
          <CardDescription>
            Имя и длительность занятия по умолчанию
          </CardDescription>
        </CardHeader>
        <CardContent>
          <FieldGroup>
            <Field data-invalid={!!errors.teacher_name}>
              <FieldLabel htmlFor="teacher_name">Имя репетитора</FieldLabel>
              <Input
                id="teacher_name"
                autoComplete="name"
                aria-invalid={!!errors.teacher_name}
                {...register("teacher_name")}
              />
              <FieldError errors={[errors.teacher_name]} />
            </Field>
            <Field data-invalid={!!errors.default_lesson_duration_minutes}>
              <FieldLabel htmlFor="default_lesson_duration_minutes">
                Длительность занятия по умолчанию (мин)
              </FieldLabel>
              <Input
                id="default_lesson_duration_minutes"
                type="number"
                min={15}
                max={240}
                aria-invalid={!!errors.default_lesson_duration_minutes}
                {...register("default_lesson_duration_minutes", {
                  valueAsNumber: true,
                })}
              />
              <FieldError errors={[errors.default_lesson_duration_minutes]} />
            </Field>
          </FieldGroup>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Автоматические напоминания</CardTitle>
          <CardDescription>
            Напоминания через Telegram-бота ученикам
          </CardDescription>
        </CardHeader>
        <CardContent>
          <FieldGroup>
            <Field data-invalid={!!errors.lesson_reminder_hours_before}>
              <FieldLabel htmlFor="lesson_reminder_hours_before">
                Напоминание о занятии за N часов
              </FieldLabel>
              <FieldDescription>
                За сколько часов до начала занятия бот отправит напоминание в
                Telegram.
              </FieldDescription>
              <Input
                id="lesson_reminder_hours_before"
                type="number"
                min={1}
                max={168}
                aria-invalid={!!errors.lesson_reminder_hours_before}
                {...register("lesson_reminder_hours_before", {
                  valueAsNumber: true,
                })}
              />
              <FieldError errors={[errors.lesson_reminder_hours_before]} />
            </Field>
            <Field data-invalid={!!errors.homework_reminder_hours_before}>
              <FieldLabel htmlFor="homework_reminder_hours_before">
                Напоминание о несданном ДЗ за N часов
              </FieldLabel>
              <FieldDescription>
                За сколько часов до дедлайна ДЗ бот напомнит о сдаче в Telegram.
              </FieldDescription>
              <Input
                id="homework_reminder_hours_before"
                type="number"
                min={1}
                max={336}
                aria-invalid={!!errors.homework_reminder_hours_before}
                {...register("homework_reminder_hours_before", {
                  valueAsNumber: true,
                })}
              />
              <FieldError errors={[errors.homework_reminder_hours_before]} />
            </Field>
          </FieldGroup>
        </CardContent>
        <CardFooter className="flex flex-wrap gap-2">
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? (
              <Spinner className="size-4" />
            ) : (
              <Save data-icon="inline-start" />
            )}
            Сохранить
          </Button>
          <Button
            type="button"
            variant="outline"
            disabled={isSubmitting}
            onClick={onReset}
          >
            Сбросить
          </Button>
        </CardFooter>
      </Card>
    </form>
  )
}
