"use client"

import { useCallback, useEffect, useRef, useState } from "react"
import { format, parseISO } from "date-fns"
import { ru } from "date-fns/locale"
import { Loader2 } from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { clientApiFetch } from "@/lib/api-client"
import { cn } from "@/lib/utils"
import type { DialogueFeedResponse, DialogueMessage } from "@/lib/types/students"

const PAGE = 20

function toChronological(items: DialogueMessage[]): DialogueMessage[] {
  return [...items].reverse()
}

type StudentDialogueFeedProps = {
  studentId: string
  /** Первая страница с API (новые сообщения первыми). */
  initialItems: DialogueMessage[]
  initialTotal: number
}

export function StudentDialogueFeed({
  studentId,
  initialItems,
  initialTotal,
}: StudentDialogueFeedProps) {
  const [messages, setMessages] = useState<DialogueMessage[]>(() =>
    toChronological(initialItems),
  )
  const [nextOffset, setNextOffset] = useState(initialItems.length)
  const [loading, setLoading] = useState(false)
  const hasMore = nextOffset < initialTotal

  const scrollRef = useRef<HTMLDivElement>(null)
  const sentinelRef = useRef<HTMLDivElement>(null)
  const firstLayout = useRef(true)

  useEffect(() => {
    const el = scrollRef.current
    if (!el || !firstLayout.current) {
      return
    }
    firstLayout.current = false
    el.scrollTop = el.scrollHeight
  }, [])

  const loadOlder = useCallback(async () => {
    if (loading || !hasMore) {
      return
    }
    const el = scrollRef.current
    const prevHeight = el?.scrollHeight
    const prevTop = el?.scrollTop
    setLoading(true)
    try {
      const res = await clientApiFetch<DialogueFeedResponse>(
        `/v1/students/${studentId}/dialogue?limit=${PAGE}&offset=${nextOffset}`,
      )
      const older = toChronological(res.items)
      setMessages((prev) => [...older, ...prev])
      setNextOffset((o) => o + res.items.length)
      requestAnimationFrame(() => {
        const box = scrollRef.current
        if (box && prevHeight !== undefined && prevTop !== undefined) {
          box.scrollTop = box.scrollHeight - prevHeight + prevTop
        }
      })
    } finally {
      setLoading(false)
    }
  }, [hasMore, loading, nextOffset, studentId])

  useEffect(() => {
    const root = scrollRef.current
    const target = sentinelRef.current
    if (!root || !target) {
      return
    }
    const obs = new IntersectionObserver(
      (entries) => {
        const hit = entries.some((e) => e.isIntersecting)
        if (hit) {
          void loadOlder()
        }
      },
      { root, rootMargin: "80px", threshold: 0 },
    )
    obs.observe(target)
    return () => obs.disconnect()
  }, [loadOlder])

  return (
    <Card className="flex max-h-[420px] flex-col overflow-hidden">
      <CardHeader className="shrink-0 pb-2">
        <CardTitle className="text-base">Диалог с ботом</CardTitle>
      </CardHeader>
      <CardContent className="min-h-0 flex-1 px-2 pb-3">
        <div
          ref={scrollRef}
          className="flex max-h-[340px] flex-col gap-2 overflow-y-auto px-2 pb-2"
        >
          <div ref={sentinelRef} className="h-1 shrink-0" aria-hidden />
          {loading ? (
            <div className="text-muted-foreground flex justify-center py-2 text-xs">
              <Loader2 className="size-4 animate-spin" />
            </div>
          ) : null}
          {messages.length === 0 ? (
            <p className="text-muted-foreground py-6 text-center text-sm">
              Сообщений пока нет.
            </p>
          ) : (
            messages.map((m) => {
              const isUser = m.role === "user"
              const t = format(parseISO(m.created_at), "d MMM, HH:mm", {
                locale: ru,
              })
              return (
                <div
                  key={m.id}
                  className={cn(
                    "flex w-full",
                    isUser ? "justify-end" : "justify-start",
                  )}
                >
                  <div
                    className={cn(
                      "max-w-[85%] rounded-lg px-3 py-2 text-sm shadow-sm",
                      isUser
                        ? "bg-primary text-primary-foreground"
                        : "bg-muted text-foreground",
                    )}
                  >
                    <p className="whitespace-pre-wrap break-words">
                      {m.content}
                    </p>
                    <p
                      className={cn(
                        "mt-1 text-[10px] opacity-80",
                        isUser ? "text-primary-foreground/80" : "",
                      )}
                    >
                      {t}
                    </p>
                  </div>
                </div>
              )
            })
          )}
        </div>
      </CardContent>
    </Card>
  )
}
