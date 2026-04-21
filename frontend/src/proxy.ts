import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"
import { jwtVerify } from "jose"

import { ACCESS_TOKEN_COOKIE } from "@/lib/constants"

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl

  if (
    pathname.startsWith("/_next") ||
    pathname.startsWith("/api/") ||
    pathname === "/favicon.ico"
  ) {
    return NextResponse.next()
  }

  const token = request.cookies.get(ACCESS_TOKEN_COOKIE)?.value
  const secret = process.env.AUTH_SECRET

  if (!token) {
    if (pathname === "/login") {
      return NextResponse.next()
    }
    return NextResponse.redirect(new URL("/login", request.url))
  }

  if (!secret) {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  let role: string
  try {
    const { payload } = await jwtVerify(
      token,
      new TextEncoder().encode(secret),
      { algorithms: ["HS256"] },
    )
    role = String(payload.role ?? "")
  } catch {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  if (pathname === "/login") {
    return NextResponse.redirect(
      new URL(
        role === "teacher" ? "/teacher/calendar" : "/student/schedule",
        request.url,
      ),
    )
  }

  if (pathname === "/") {
    return NextResponse.redirect(
      new URL(
        role === "teacher" ? "/teacher/calendar" : "/student/schedule",
        request.url,
      ),
    )
  }

  if (pathname.startsWith("/teacher") && role !== "teacher") {
    return NextResponse.redirect(new URL("/student/schedule", request.url))
  }
  if (pathname.startsWith("/student") && role !== "student") {
    return NextResponse.redirect(new URL("/teacher/calendar", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|.*\\.(?:ico|png|svg|webp|woff2?)$).*)",
  ],
}
