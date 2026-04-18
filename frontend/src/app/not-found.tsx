import Link from "next/link"

import { buttonVariants } from "@/components/ui/button"
import { cn } from "@/lib/utils"

export default function NotFound() {
  return (
    <div className="flex min-h-[50vh] flex-col items-center justify-center gap-4 p-8">
      <h1 className="text-2xl font-semibold">Страница не найдена</h1>
      <p className="text-muted-foreground text-center text-sm">
        Запрошенный адрес не существует.
      </p>
      <Link href="/" className={cn(buttonVariants())}>
        На главную
      </Link>
    </div>
  )
}
