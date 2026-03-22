# Как получить токен бота и API-ключ OpenRouter

Краткие шаги без секретов в тексте: ключи и токены нигде не публиковать и не коммитить — только в `.env` (см. `.env.example`).

## Telegram: бот и токен

1. Откройте в Telegram бота [@BotFather](https://t.me/botfather).
2. Отправьте команду `/newbot`.
3. Задайте **отображаемое имя** бота (как его видят пользователи).
4. Задайте **username** бота: должен заканчиваться на `bot`, быть уникальным в Telegram.
5. BotFather пришлёт **токен доступа к HTTP API** — сохраните его в надёжном месте; это секрет, как пароль.

Дополнительно по смыслу команд и полям — разделы официальной документации:

- [Создание нового бота](https://core.telegram.org/bots/features#creating-a-new-bot)
- [BotFather](https://core.telegram.org/bots/features#botfather)
- [Туториал: получение токена](https://core.telegram.org/bots/tutorial) (блок про токен в начале статьи)

При утечке токена отзовите его и получите новый в [@BotFather](https://t.me/botfather): `/mybots` → ваш бот → раздел с токеном API.

## OpenRouter: аккаунт и API key

1. Зайдите на [openrouter.ai](https://openrouter.ai) и зарегистрируйтесь или войдите.
2. При необходимости пополните баланс на странице [Credits](https://openrouter.ai/settings/credits) (для платных моделей; стартовый сценарий описан в [FAQ](https://openrouter.ai/docs/faq#how-do-i-get-started-with-openrouter)).
3. Создайте ключ на странице [Keys](https://openrouter.ai/keys): задайте имя ключа, при желании лимит по кредитам.
4. Скопируйте ключ сразу после создания и сохраните в `.env`; повторно полный ключ может быть недоступен — при потере создайте новый в [настройках ключей](https://openrouter.ai/settings/keys).

Официальные материалы по использованию ключа в запросах:

- [Аутентификация API (Bearer)](https://openrouter.ai/docs/api/reference/authentication)
- [Quickstart](https://openrouter.ai/docs/quickstart)

Ключ передаётся как `Authorization: Bearer <ваш_ключ>`; не вставляйте его в чаты, скриншоты и публичные репозитории.
