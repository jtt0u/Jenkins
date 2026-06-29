# Jenkins Sample Application

Простое Node.js приложение для практических заданий курса по Jenkins.

## Описание

Это Express приложение демонстрирует работу с:
- Environment переменными
- Credentials
- Parameters в Jenkins Pipeline
- Сборкой и тестированием приложения

## Установка

```bash
npm install
```

## Переменные окружения

Приложение использует следующие переменные окружения:

| Переменная | Описание | Значение по умолчанию |
|-----------|----------|---------------------|
| `PORT` | Порт для запуска сервера | `3000` |
| `NODE_ENV` | Окружение (development/staging/production) | `development` |
| `APP_VERSION` | Версия приложения | `1.0.0` |
| `BUILD_NUMBER` | Номер сборки из Jenkins | `local` |
| `API_KEY` | API ключ (пример для credentials) | `not-set` |
| `DATABASE_URL` | URL базы данных (пример для credentials) | `not-configured` |

## Запуск

### Локально

```bash
npm start
```

Приложение будет доступно по адресу: `http://localhost:3000`

### С переменными окружения

```bash
NODE_ENV=production APP_VERSION=1.0.0 BUILD_NUMBER=42 npm start
```

## API Endpoints

### GET /
Основная информация о приложении
```json
{
  "status": "running",
  "message": "Jenkins Sample Application",
  "environment": "development",
  "version": "1.0.0",
  "build": "local",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

### GET /health
Проверка работоспособности
```json
{
  "status": "healthy",
  "uptime": 123.456,
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

### GET /config
Конфигурация приложения
```json
{
  "environment": "development",
  "version": "1.0.0",
  "build": "local",
  "port": "3000",
  "apiKeyConfigured": false,
  "databaseConfigured": false
}
```

### GET /info
Информация о системе
```json
{
  "nodeVersion": "v18.0.0",
  "platform": "linux",
  "architecture": "x64",
  "memory": {
    "total": "50 MB",
    "used": "30 MB"
  }
}
```

## Тестирование

```bash
npm test
```

Тесты проверяют:
- Наличие необходимых переменных окружения
- Валидность формата версии
- Корректность значения окружения
- Наличие зависимостей

## Сборка

```bash
npm run build
```

Создаёт директорию `dist/` с файлами приложения.

## Использование в Jenkins Pipeline

### Пример с environment переменными

```groovy
pipeline {
    agent any
    environment {
        NODE_ENV = 'production'
        APP_VERSION = '1.0.0'
    }
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
    }
}
```

### Пример с credentials

```groovy
pipeline {
    agent any
    stages {
        stage('Deploy') {
            steps {
                withCredentials([string(credentialsId: 'api-key', variable: 'API_KEY')]) {
                    sh 'API_KEY=$API_KEY npm start &'
                }
            }
        }
    }
}
```

### Пример с parameters

```groovy
pipeline {
    agent any
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['development', 'staging', 'production'])
        string(name: 'VERSION', defaultValue: '1.0.0')
    }
    stages {
        stage('Deploy') {
            steps {
                sh "NODE_ENV=${params.ENVIRONMENT} APP_VERSION=${params.VERSION} npm start"
            }
        }
    }
}
```

## Структура проекта

```
sample-app/
├── server.js          # Основной файл приложения
├── test.js            # Тесты
├── package.json       # Зависимости и скрипты
├── .env.example       # Пример файла с переменными
├── .gitignore         # Игнорируемые файлы
└── README.md          # Документация
```

## Лицензия

MIT
