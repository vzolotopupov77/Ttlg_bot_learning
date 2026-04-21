# Итерация 6 — Расписание ученика — Summary

**Статус:** ✅ **Итерация закрыта** — реализация **2026-04-21**, ручная приёмка подтверждена пользователем (чекбоксы ниже). Дополнение **2026-04-22:** исправлена загрузка `.env` для Alembic; смена пароля ученика через `downgrade`/`upgrade` с `STUDENT_DEFAULT_PASSWORD` в корневом `.env` проверена — работает корректно.

## Что сделано

- **`/student/schedule`:** [`page.tsx`](../../../../../frontend/src/app/(app)/student/schedule/page.tsx) — Server Component: `getUser`, редиректы, `fetchStudentSchedule(weekStart)`, `parseWeekStart` из query.
- **`StudentScheduleView`** — [`student-schedule-view.tsx`](../../../../../frontend/src/components/student-schedule-view.tsx): заголовок «Расписание — {ФИО}», `WeeklySchedule` с `basePath="/student/schedule"`, без `onAddLesson`, клик по занятию → `Sheet` (тема, дата, время, статус, `LessonFlagsRow`).
- **`WeeklySchedule`** — опциональные `basePath`, `onOpenLesson`, `onAddLesson`; ссылки навигации строятся от `basePath`.
- **`LessonCard`** — опциональный `onOpen` (без колбэка — статичный блок).
- **`fetchStudentSchedule`** — [`api-server.ts`](../../../../../frontend/src/lib/api-server.ts) → `GET /v1/student/schedule?week_start=`.
- **БД:** миграция [`e1f2a3b4c5d6_seed_student_web_password.py`](../../../../../backend/alembic/versions/e1f2a3b4c5d6_seed_student_web_password.py) — `UPDATE users SET password_hash = ...` для `alex@example.com` (seed из `b8c9d0e1f2a3`); пароль из `STUDENT_DEFAULT_PASSWORD` (см. [`.env.example`](../../../../../.env.example)).
- **Alembic / `.env`:** [`env.py`](../../../../../backend/alembic/env.py) — `load_dotenv(_REPO_ROOT / ".env")`, чтобы миграции всегда видели переменные из **корневого** `.env` (не зависят от cwd при `uv run alembic`). Без этого миграция пароля ученика могла брать только дефолт из кода.

## Самопроверки (агент)

Выполнены **2026-04-21**, корень репозитория `Ttlg_bot_learning` (Windows / PowerShell).

| Проверка | Команда | Результат |
|----------|---------|-----------|
| TypeScript | `cd frontend; pnpm exec tsc --noEmit` | Успех, exit 0 |
| ESLint | `make frontend-lint` | Успех, exit 0; **1 warning** в `lesson-dialog.tsx` (`react-hooks/exhaustive-deps`) — вне итерации 6 |
| Сборка Next.js | `make frontend-build` | Успех, exit 0; маршрут `/student/schedule` |
| Ruff (миграция) | `uv run ruff check backend/alembic/versions/e1f2a3b4c5d6_seed_student_web_password.py` | Успех, exit 0 |
| Ruff (`env.py`) | `uv run ruff check backend/alembic/env.py` | Успех, exit 0 (после правки загрузки `.env`) |

## Ручные проверки (пользователь)

**Предусловие:** `make backend-db-migrate` (новая миграция), backend и frontend запущены. Вход: `alex@example.com` / пароль из `STUDENT_DEFAULT_PASSWORD` (по умолчанию `changeme_student`), роль **Ученик**.

| Шаг | Сценарий | Результат |
|-----|----------|-----------|
| 1 | Войти как ученик → `/student/schedule` | OK |
| 2 | Недельная сетка, «Нет занятий» или карточки | OK |
| 3 | «‹ / Сегодня / ›» — смена недели | OK |
| 4 | Клик по занятию — `Sheet` с темой, временем, флагами | OK |
| 5 | Кнопки «+ Занятие» нет | OK |

## Пароль тестового ученика (`STUDENT_DEFAULT_PASSWORD`) и миграции

Хэш пароля для `alex@example.com` записывается **один раз** в `upgrade()` миграции `e1f2a3b4c5d6`: при первом применении берётся значение переменной окружения `STUDENT_DEFAULT_PASSWORD` (или default из кода). Запись в таблице `alembic_version` означает, что повторный `make backend-db-migrate` **не выполняет** этот `upgrade` снова — смена пароля в `.env` и перезапуск backend **не меняют** `password_hash` в БД.

**Почему мог остаться пароль как в `.env.example` (дефолт в коде):** до правки `backend/alembic/env.py` `load_dotenv()` без пути искал `.env` от **текущей рабочей директории**. При некоторых способах запуска `uv` cwd не был корнем репозитория — переменная не подхватывалась, миграция брала default `changeme_student`. Сейчас `.env` грузится **явно** из корня репо (относительно `env.py`).

**Как задать новый пароль после того, как миграция уже применена:**

1. Убедитесь, что `STUDENT_DEFAULT_PASSWORD` задан в **`.env` в корне репозитория** (рядом с `Makefile`).
2. Откат и повторное применение ревизии пароля:
   - `uv run --package ttlg-backend alembic -c backend/alembic.ini downgrade c9d0e1f2a3b4`
   - `uv run --package ttlg-backend alembic -c backend/alembic.ini upgrade head`
3. Либо вручную обновить `users.password_hash` (bcrypt), без повторного прогона миграции.

**Фиксация после приёмки:** пользователь подтвердил, что после правки `env.py` повторный `downgrade c9d0e1f2a3b4` → `upgrade head` с нужным `STUDENT_DEFAULT_PASSWORD` в корневом `.env` задаёт пароль в БД ожидаемо (не дефолт из `.env.example`).

## Закрытие итерации

Прогресс в [tasklist-frontend.md](../../../tasks/tasklist-frontend.md) синхронизирован; итерация 6 закрыта по коду, ручной приёмке экрана и проверке сценария смены пароля ученика.
