import { Skeleton } from "@/components/ui/skeleton"

export default function SettingsLoading() {
  return (
    <div className="flex flex-col gap-4 p-2">
      <Skeleton className="h-8 w-40" />
      <Skeleton className="h-32 w-full max-w-md" />
    </div>
  )
}
