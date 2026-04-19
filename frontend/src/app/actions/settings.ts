"use server"

import { revalidatePath } from "next/cache"

import { serverApiFetch } from "@/lib/api-server"
import { translateApiErrorMessage } from "@/lib/api-error-messages"
import type { SystemSettings } from "@/lib/types/settings"

function fail(e: unknown): { ok: false; error: string } {
  const raw = e instanceof Error ? e.message : String(e)
  return { ok: false, error: translateApiErrorMessage(raw) }
}

export async function updateSettingsAction(
  body: SystemSettings,
): Promise<{ ok: true; settings: SystemSettings } | { ok: false; error: string }> {
  try {
    const settings = await serverApiFetch<SystemSettings>("/v1/settings", {
      method: "PUT",
      body: JSON.stringify(body),
    })
    revalidatePath("/teacher/settings")
    return { ok: true, settings }
  } catch (e) {
    return fail(e)
  }
}
