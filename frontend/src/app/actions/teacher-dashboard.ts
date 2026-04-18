"use server"

import { revalidatePath } from "next/cache"

import { serverApiFetch } from "@/lib/api-server"
import { translateApiErrorMessage } from "@/lib/api-error-messages"
import type { RemindResponse } from "@/lib/types/teacher-calendar"

function fail(e: unknown): { ok: false; error: string } {
  const raw = e instanceof Error ? e.message : String(e)
  return { ok: false, error: translateApiErrorMessage(raw) }
}

export async function remindUnconfirmedAction(): Promise<
  { ok: true; notified_count: number } | { ok: false; error: string }
> {
  try {
    const res = await serverApiFetch<RemindResponse>(
      "/v1/teacher/remind-unconfirmed",
      { method: "POST" },
    )
    revalidatePath("/teacher/calendar")
    return { ok: true, notified_count: res.notified_count }
  } catch (e) {
    return fail(e)
  }
}

export async function remindPendingHomeworkAction(): Promise<
  { ok: true; notified_count: number } | { ok: false; error: string }
> {
  try {
    const res = await serverApiFetch<RemindResponse>(
      "/v1/teacher/remind-pending-homework",
      { method: "POST" },
    )
    revalidatePath("/teacher/calendar")
    return { ok: true, notified_count: res.notified_count }
  } catch (e) {
    return fail(e)
  }
}

export async function patchRescheduleRequestAction(
  requestId: string,
  status: "accepted" | "rejected",
): Promise<{ ok: true } | { ok: false; error: string }> {
  try {
    await serverApiFetch(`/v1/teacher/reschedule-requests/${requestId}`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    })
    revalidatePath("/teacher/calendar")
    return { ok: true }
  } catch (e) {
    return fail(e)
  }
}
