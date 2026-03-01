# Scripts

## local-test.sh

Запускает тесты локально перед коммитом. Использует Docker Compose для поднятия базы данных и Redis.

### Использование

```bash
# Сделать скрипт исполняемым
chmod +x scripts/local-test.sh

# Запустить тесты
./scripts/local-test.sh
```

### Что делает:
1. Проверяет наличие `.env` файла (создает из `.env.example` если нет)
2. Проверяет что Docker запущен
3. Поднимает PostgreSQL и Redis контейнеры
4. Запускает миграции
5. Запускает тесты `api.tests`
6. Показывает результат

### Выход:
- `0` - все тесты прошли ✅
- `1` - есть упавшие тесты ❌

---

## pre-commit

Git hook для автоматического запуска тестов перед каждым коммитом.

### Установка

```bash
# Скопировать в git hooks
cp scripts/pre-commit .git/hooks/pre-commit

# Сделать исполняемым
chmod +x .git/hooks/pre-commit
```

### Использование

После установки скрипт будет автоматически запускаться при каждой попытке сделать коммит:

```bash
git commit -m "your message"
# pre-commit hook запустится автоматически
```

Если тесты падают - коммит отменяется.

### Отключение

```bash
# Временное отключение
git commit --no-verify -m "your message"

# Полное удаление
rm .git/hooks/pre-commit
```

---

## GitHub Actions

Тесты также запускаются автоматически при push и pull request в GitHub.

Конфигурация: `.github/workflows/test.yml`

### Триггеры:
- Push в ветки: `backend`, `main`, `master`
- Pull request в ветки: `backend`, `main`, `master`

### Что делает:
1. Устанавливает Python 3.12
2. Поднимает PostgreSQL и Redis (GitHub Actions services)
3. Устанавливает зависимости
4. Создает `.env` файл
5. Запускает миграции
6. Запускает тесты
7. Сохраняет результаты тестов

---

## Рекомендуемый workflow

1. **Перед коммитом:**
   ```bash
   ./scripts/local-test.sh
   ```

2. **Или установите pre-commit hook:**
   ```bash
   cp scripts/pre-commit .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```

3. **После коммита:**
   - GitHub Actions автоматически запустит тесты
   - Результаты будут видны в GitHub Actions tab
