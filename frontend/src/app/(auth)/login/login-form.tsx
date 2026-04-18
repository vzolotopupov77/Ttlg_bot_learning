"use client"

import { GraduationCap, LogIn } from "lucide-react"
import { useActionState, useState } from "react"

import { loginAction, type LoginState } from "@/app/actions/auth"
import { ThemeToggle } from "@/components/theme-toggle"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Field,
  FieldContent,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Spinner } from "@/components/ui/spinner"

const initialState: LoginState = null

export function LoginForm() {
  const [role, setRole] = useState<"teacher" | "student">("teacher")
  const [state, formAction, isPending] = useActionState(
    loginAction,
    initialState,
  )

  return (
    <div className="relative flex min-h-full flex-1 flex-col items-center justify-center p-6">
      <div className="absolute right-4 top-4">
        <ThemeToggle />
      </div>
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="mx-auto mb-2 flex size-12 items-center justify-center rounded-lg bg-primary/10">
            <GraduationCap className="size-7 text-primary" />
          </div>
          <CardTitle>Репетитор</CardTitle>
          <CardDescription>
            Выберите роль и войдите в систему
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form action={formAction} className="flex flex-col gap-5">
            <input type="hidden" name="role" value={role} />
            <div className="flex flex-col gap-2">
              <span className="text-sm font-medium">Роль</span>
              <div className="flex gap-2">
                <Button
                  type="button"
                  variant={role === "teacher" ? "default" : "outline"}
                  className="flex-1"
                  onClick={() => setRole("teacher")}
                >
                  Преподаватель
                </Button>
                <Button
                  type="button"
                  variant={role === "student" ? "default" : "outline"}
                  className="flex-1"
                  onClick={() => setRole("student")}
                >
                  Ученик
                </Button>
              </div>
            </div>
            <FieldGroup>
              <Field>
                <FieldLabel htmlFor="email">E-mail</FieldLabel>
                <FieldContent>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    placeholder="you@example.com"
                  />
                </FieldContent>
              </Field>
              <Field>
                <FieldLabel htmlFor="password">Пароль</FieldLabel>
                <FieldContent>
                  <Input
                    id="password"
                    name="password"
                    type="password"
                    autoComplete="current-password"
                    required
                  />
                </FieldContent>
              </Field>
            </FieldGroup>
            {state?.error ? (
              <Alert variant="destructive">
                <AlertDescription>{state.error}</AlertDescription>
              </Alert>
            ) : null}
            <Button type="submit" className="w-full" disabled={isPending}>
              {isPending ? (
                <Spinner className="size-4" />
              ) : (
                <LogIn className="size-4" />
              )}
              <span>{isPending ? "Вход…" : "Войти"}</span>
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
