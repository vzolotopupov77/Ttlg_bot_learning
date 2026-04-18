"use client"

import { useEffect } from "react"

import { Button } from "@/components/ui/button"

export default function AppError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div className="flex flex-col items-center justify-center gap-4 p-8">
      <h2 className="text-lg font-semibold">Что-то пошло не так</h2>
      <p className="text-muted-foreground text-center text-sm">
        {error.message || "Попробуйте обновить страницу."}
      </p>
      <Button type="button" onClick={() => reset()}>
        Повторить
      </Button>
    </div>
  )
}
