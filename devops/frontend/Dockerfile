# syntax=docker/dockerfile:1
# Контекст сборки: корень репозитория. Lockfile — корневой pnpm-lock.yaml (workspace).
FROM node:20-alpine AS deps

RUN corepack enable && corepack prepare pnpm@9.15.4 --activate

WORKDIR /app

COPY pnpm-workspace.yaml pnpm-lock.yaml ./
COPY frontend/package.json ./frontend/

RUN pnpm install --frozen-lockfile --filter frontend...

FROM deps AS builder

COPY frontend/ ./frontend/

WORKDIR /app/frontend

ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_TELEMETRY_DISABLED=1

RUN pnpm run build

FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nodejs

# Monorepo: не «сплющивать» standalone — symlinks в node_modules рассчитаны на корень + подкаталог frontend/
COPY --from=builder --chown=nodejs:nodejs /app/frontend/.next/standalone ./
COPY --from=builder --chown=nodejs:nodejs /app/frontend/.next/static ./frontend/.next/static
COPY --from=builder --chown=nodejs:nodejs /app/frontend/public ./frontend/public

WORKDIR /app/frontend

USER nodejs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME=0.0.0.0

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD node -e "fetch('http://127.0.0.1:3000/').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

CMD ["node", "server.js"]
