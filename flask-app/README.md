# Flask Application для Jenkins Module 7

Веб-приложение на Flask для демонстрации интеграции с Git, Multibranch Pipeline, деплоя на различные окружения, тестирования и уведомлений.

## Возможности

- HTTP API с несколькими endpoints
- Health check для мониторинга
- Метрики приложения
- Поддержка разных окружений (dev, staging, production)
- Информация о Git коммите и ветке
- Unit тесты с coverage
- Docker контейнеризация
- Multi-stage Dockerfile

## API Endpoints

### Основные
- `GET /` - Главная страница с информацией о приложении
- `GET /health` - Health check endpoint
- `GET /api/info` - Детальная информация о приложении
- `GET /api/metrics` - Метрики и статистика
- `GET /api/config` - Текущая конфигурация
- `GET /api/status` - Детальный статус приложения

### Mock API
- `GET /api/users` - Список пользователей (mock data)
- `POST /api/users` - Создание пользователя (mock endpoint)

## Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `PORT` | Порт HTTP сервера | `5000` |
| `APP_VERSION` | Версия приложения | `dev` |
| `ENVIRONMENT` | Окружение (dev/staging/production) | `development` |
| `BUILD_TIME` | Время сборки | текущее время |
| `GIT_COMMIT` | Git commit hash | `unknown` |
| `GIT_BRANCH` | Git branch | `unknown` |

## Запуск локально

### Без Docker

```bash
# Установка зависимостей
make install

# Запуск в development режиме
make run

# Запуск в production режиме
make run-prod VERSION=1.0.0

# Тесты
make test

# Тесты с coverage
make test-coverage

# Линтеры
make lint
```

### С Docker

```bash
# Сборка образа
make docker-build VERSION=1.0.0

# Запуск контейнера (development)
make docker-run VERSION=1.0.0

# Запуск контейнера (production)
make docker-run-prod VERSION=1.0.0

# Или через docker-compose
APP_VERSION=1.0.0 ENVIRONMENT=production docker-compose up
```

## Тестирование

Приложение имеет 15 unit тестов, покрывающих все endpoints:

```bash
# Запуск тестов
pytest test_app.py -v

# С coverage отчётом
pytest test_app.py -v --cov=app --cov-report=html

# Открыть coverage отчёт
open htmlcov/index.html
```

## Использование в Jenkins

Это приложение используется в практиках модуля 7 для демонстрации:

### Практика 7.2 - Интеграция с Git
- Клонирование репозитория
- Работа с разными ветками
- Использование Git переменных (GIT_COMMIT, GIT_BRANCH)
- Создание Git тегов

### Практика 7.4 - Multibranch Pipeline
- Автоматическое обнаружение веток
- Условное выполнение для разных веток
- Pull Request обнаружение

### Практика 7.6 - Деплой на различные окружения
- Деплой на dev, staging, production
- Управление конфигурациями окружений
- Использование параметров для выбора окружения
- Работа с секретами

### Практика 7.8 - Тестирование в пайплайнах
- Unit тесты с coverage
- Сбор результатов тестов (JUnit XML)
- Публикация coverage отчётов
- Параллельное выполнение тестов

### Практика 7.10 - Итоговое задание
- Комплексный пайплайн с Git, тестами, деплоем и уведомлениями
- Notifications в Slack/Email
- Условное выполнение стейджей
- Ручное подтверждение для production

## Структура проекта

```
flask-app/
├── app.py                  # Основной код приложения
├── test_app.py            # Unit тесты
├── requirements.txt       # Python зависимости
├── Dockerfile             # Production Dockerfile (multi-stage)
├── .dockerignore          # Исключения для Docker контекста
├── docker-compose.yml     # Docker Compose конфигурация
├── Makefile               # Автоматизация задач
├── pytest.ini             # Конфигурация pytest
└── README.md              # Документация
```

## Примеры запросов

```bash
# Health check
curl http://localhost:5000/health

# Информация о приложении
curl http://localhost:5000/api/info

# Метрики
curl http://localhost:5000/api/metrics

# Список пользователей
curl http://localhost:5000/api/users

# Создание пользователя
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

## Размер образов

- **Development**: ~150MB (с зависимостями для тестирования)
- **Production** (multi-stage): ~80MB (только runtime зависимости)

Multi-stage build значительно уменьшает размер production образа, убирая build tools и тестовые зависимости.

## Конфигурация окружений

Приложение автоматически подстраивается под окружение через переменную `ENVIRONMENT`:

- **development**: Debug mode включен, подробные логи
- **staging**: Приближено к production, но с дополнительным логированием
- **production**: Минимальное логирование, оптимизация производительности

## Healthcheck

Docker образ включает healthcheck, который проверяет `/health` endpoint каждые 30 секунд. Kubernetes/Docker Swarm используют это для определения готовности контейнера.
