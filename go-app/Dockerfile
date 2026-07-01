# Multi-stage build для оптимального размера образа
FROM golang:1.21 AS builder

WORKDIR /build

# Копируем go.mod и go.sum для кэширования зависимостей
COPY go.mod go.sum* ./
RUN go mod download || true

# Копируем исходный код
COPY . .

# Принимаем аргументы сборки
ARG APP_VERSION=dev
ARG BUILD_TIME
ARG GIT_COMMIT=unknown
ARG BUILD_NUMBER=local

# Компилируем приложение со встроенными переменными
RUN CGO_ENABLED=0 GOOS=linux go build \
    -ldflags "-X main.version=${APP_VERSION} -X main.buildTime=${BUILD_TIME} -X main.gitCommit=${GIT_COMMIT}" \
    -o app .

# Финальный образ - минимальный размер
FROM alpine:latest

# Установка ca-certificates для HTTPS запросов
RUN apk --no-cache add ca-certificates tzdata

WORKDIR /app

# Копируем бинарник из builder стадии
COPY --from=builder /build/app .

# Создаём непривилегированного пользователя
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /app

USER appuser

# Переменные окружения по умолчанию
ENV PORT=8080 \
    ENVIRONMENT=production \
    APP_VERSION=${APP_VERSION}

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

CMD ["./app"]
