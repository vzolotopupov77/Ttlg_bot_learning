# Задача 03: Обновить `.cursor/rules/conventions.mdc`

## Цель

Добавить в правила Cursor явные ориентиры для backend, согласованные с [docs/vision.md](../../../../../vision.md) и [ADR-002](../../../../../adr/adr-002-orm-migrations-tests.md).

## Что меняется

- Файл [.cursor/rules/conventions.mdc](../../../../../../.cursor/rules/conventions.mdc): новая секция **Backend** (пакет, слои, поток запроса, async, тесты, Makefile).

## Ограничения

- Не расширять стек сверх vision; новые инструменты — только через правку vision + ADR.

## Definition of Done

- Секция backend присутствует; убраны/не допускаются формулировки про «только бот без БД» как единственную модель.
