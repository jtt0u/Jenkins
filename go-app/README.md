# Go Application для Jenkins Module 6

Простое HTTP приложение на Go для демонстрации работы с Docker в Jenkins пайплайнах.

## Возможности

- HTTP сервер с несколькими эндпоинтами
- Health check для мониторинга
- Метрики приложения
- Поддержка переменных окружения
- Multi-stage Dockerfile для оптимизации размера образа
- Dockerfile для CI с предустановленными инструментами
- Unit тесты с coverage
- Makefile для автоматизации задач

## Эндпоинты

- `GET /` - Главная страница с информацией о приложении
- `GET /health` - Health check (для Kubernetes/Docker healthchecks)
- `GET /info` - Детальная информация о приложении
- `GET /metrics` - Метрики приложения (память, goroutines, счётчики)
- `GET /api/data` - Пример API эндпоинта с данными

## Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `PORT` | Порт для HTTP сервера | `8080` |
| `APP_VERSION` | Версия приложения | `dev` |
| `ENVIRONMENT` | Окружение (dev/staging/prod) | `development` |
| `BUILD_TIME` | Время сборки | текущее время |
| `GIT_COMMIT` | Git commit hash | `unknown` |
| `BUILD_NUMBER` | Номер билда | - |
| `CUSTOM_METRICS` | Включить кастомные метрики | `false` |
| `METADATA_KEYS` | Включить метаданные | - |
| `METADATA_KEY1-5` | Кастомные метаданные | - |

## Запуск локально

### Без Docker

```bash
# Сборка
make build

# Запуск
make run

# Тесты
make test

# Coverage
make coverage

# Линтеры
make lint
```

### С Docker

```bash
# Сборка образа
make docker-build VERSION=1.0.0

# Запуск контейнера
make docker-run VERSION=1.0.0

# Или напрямую через docker
docker build -t go-app:1.0.0 .
docker run -p 8080:8080 -e ENVIRONMENT=production go-app:1.0.0
```

### CI образ

```bash
# Сборка CI образа (с инструментами для тестирования)
make docker-build-ci

# Запуск тестов в CI образе
docker run --rm go-app:ci go test -v ./...
```

## Использование в Jenkins

Это приложение используется в практиках модуля 6 для демонстрации:

- Сборки Docker образов в пайплайне
- Multi-stage builds для оптимизации размера
- Использования Docker агентов
- Публикации образов в registry
- Версионирования образов
- Передачи build-аргументов
- Health checks и мониторинга

## Структура проекта

```
go-app/
├── main.go           # Основной код приложения
├── main_test.go      # Unit тесты
├── go.mod            # Go модуль
├── Dockerfile        # Production Dockerfile (multi-stage)
├── Dockerfile.ci     # CI Dockerfile (с инструментами)
├── .dockerignore     # Исключения для Docker контекста
├── Makefile          # Автоматизация задач
└── README.md         # Документация
```

## Примеры запросов

```bash
# Health check
curl http://localhost:8080/health

# Информация о приложении
curl http://localhost:8080/info

# Метрики
curl http://localhost:8080/metrics

# API данные
curl http://localhost:8080/api/data
```

## Размер образов

- **Production образ** (multi-stage): ~15MB
- **CI образ**: ~1.2GB (включает Go toolchain и инструменты)

Multi-stage build позволяет получить минимальный production образ, содержащий только скомпилированный бинарник.
