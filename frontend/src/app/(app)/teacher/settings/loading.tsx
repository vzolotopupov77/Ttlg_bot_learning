import { Skeleton } from "@/components/ui/skeleton"

export default function SettingsLoading() {
  return (
    <div className="flex max-w-2xl flex-col gap-6">
      <div className="flex flex-col gap-2">
        <Skeleton className="h-7 w-56" />
        <Skeleton className="h-4 w-80 max-w-full" />
      </div>
      <div className="flex flex-col gap-4 overflow-hidden rounded-xl bg-card py-4 ring-1 ring-foreground/10">
        <div className="flex flex-col gap-1 px-4">
          <Skeleton className="h-5 w-40" />
          <Skeleton className="h-4 w-64 max-w-full" />
        </div>
        <div className="flex flex-col gap-4 px-4">
          <Skeleton className="h-4 w-32" />
          <Skeleton className="h-8 w-full" />
          <Skeleton className="h-4 w-48" />
          <Skeleton className="h-8 w-full" />
        </div>
      </div>
      <div className="flex flex-col gap-4 overflow-hidden rounded-xl bg-card py-4 ring-1 ring-foreground/10">
        <div className="flex flex-col gap-1 px-4">
          <Skeleton className="h-5 w-52" />
          <Skeleton className="h-4 w-72 max-w-full" />
        </div>
        <div className="flex flex-col gap-4 px-4">
          <Skeleton className="h-4 w-56" />
          <Skeleton className="h-12 w-full" />
          <Skeleton className="h-4 w-64" />
          <Skeleton className="h-12 w-full" />
        </div>
        <div className="flex gap-2 border-t bg-muted/50 p-4">
          <Skeleton className="h-8 w-28" />
          <Skeleton className="h-8 w-24" />
        </div>
      </div>
    </div>
  )
}
