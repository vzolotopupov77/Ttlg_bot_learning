import { cache } from "react"

import { cookies } from "next/headers"

import { ACCESS_TOKEN_COOKIE, getServerApiUrl } from "@/lib/constants"

export type UserPublic = {
  id: string
  name: string
  role: "teacher" | "student"
}

export const getSession = cache(async () => {
  const cookieStore = await cookies()
  const token = cookieStore.get(ACCESS_TOKEN_COOKIE)?.value
  if (!token) {
    return null
  }
  return { token }
})

export const getUser = cache(async (): Promise<UserPublic | null> => {
  const session = await getSession()
  if (!session) {
    return null
  }
  const res = await fetch(`${getServerApiUrl()}/v1/auth/me`, {
    headers: { Cookie: `${ACCESS_TOKEN_COOKIE}=${session.token}` },
    cache: "no-store",
  })
  if (!res.ok) {
    return null
  }
  return (await res.json()) as UserPublic
})
