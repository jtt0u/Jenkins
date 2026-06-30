# Jenkins Python Application

Простое Python/Flask приложение для практических заданий курса по Jenkins. Демонстрирует работу с артефактами, workspace management, stash/unstash и другими концепциями CI/CD.

## Описание

Это веб-приложение на Flask демонстрирует:
- Генерацию различных типов артефактов (bytecode, документация, отчеты)
- Работу с переменными окружения
- Создание test coverage отчетов
- Сборку и упаковку приложения
- Управление workspace

## Требования

- Python 3.8+
- pip

## Установка

```bash
pip install -r requirements.txt
```

## Переменные окружения

Приложение использует следующие переменные окружения:

| Переменная | Описание | Значение по умолчанию |
|-----------|----------|---------------------|
| `APP_VERSION` | Версия приложения | `1.0.0` |
| `BUILD_NUMBER` | Номер сборки из Jenkins | `local` |
| `ENVIRONMENT` | Окружение (development/staging/production) | `development` |
| `PORT` | Порт для запуска сервера | `5000` |
| `DEBUG` | Режим отладки (true/false) | `false` |

## Запуск

### Локально

```bash
python app.py
```

Приложение будет доступно по адресу: `http://localhost:5000`

### С переменными окружения

```bash
APP_VERSION=1.0.0 BUILD_NUMBER=42 ENVIRONMENT=production python app.py
```

## Тестирование

### Запуск тестов

```bash
pytest
```

### С coverage отчетом

```bash
pytest --cov=app --cov-report=html --cov-report=term
```

Coverage отчет будет создан в директории `htmlcov/`

### С XML отчетом (для Jenkins)

```bash
pytest --cov=app --cov-report=xml --junit-xml=test-results.xml
```

## Сборка

### Генерация артефактов

```bash
python build.py
```

Создаст директорию `dist/` с следующими артефактами:

```
dist/
├── build-info.json          # Метаданные сборки
├── BUILD-REPORT.txt         # Отчет о сборке
├── README.md                # Документация пакета
├── compiled/                # Скомпилированный bytecode
│   └── app.pyc
├── docs/                    # API документация
│   └── API.md
└── package/                 # Готовый пакет для деплоя
    ├── app.py
    ├── requirements.txt
    ├── build-info.json
    └── VERSION
```

### Используя Makefile

```bash
make build    # Собрать артефакты
make test     # Запустить тесты
make clean    # Очистить артефакты
make run      # Запустить приложение
make lint     # Проверить код
```

## API Endpoints

### GET /
Главная страница приложения с информацией о версии и окружении.

### GET /api/info
Возвращает информацию о приложении в JSON формате:

```json
{
  "application": "jenkins-python-app",
  "version": "1.0.0",
  "build": "42",
  "environment": "production",
  "timestamp": "2024-01-01T00:00:00.000000"
}
```

### GET /api/health
Health check endpoint:

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "build": "42",
  "timestamp": "2024-01-01T00:00:00.000000"
}
```

### GET /api/metrics
Метрики приложения:

```json
{
  "application": "jenkins-python-app",
  "version": "1.0.0",
  "build": "42",
  "environment": "production",
  "metrics": {
    "python_version": "3.11.0",
    "platform": "linux"
  }
}
```

## Использование в Jenkins Pipeline

### Пример с archiveArtifacts

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'python build.py'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest --cov=app --cov-report=xml --junit-xml=test-results.xml'
            }
        }
        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'dist/**/*', fingerprint: true
                junit 'test-results.xml'
            }
        }
    }
}
```

### Пример со stash/unstash

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'python build.py'
                stash name: 'build-artifacts', includes: 'dist/**/*'
            }
        }
        stage('Deploy') {
            steps {
                unstash 'build-artifacts'
                sh 'ls -la dist/'
            }
        }
    }
}
```

### Пример с workspace management

```groovy
pipeline {
    agent any
    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Build') {
            steps {
                sh 'python build.py'
            }
        }
        stage('Archive and Clean') {
            steps {
                archiveArtifacts artifacts: 'dist/**/*'
                cleanWs(
                    deleteDirs: true,
                    patterns: [[pattern: 'dist/', type: 'EXCLUDE']]
                )
            }
        }
    }
}
```

## Структура проекта

```
python-app/
├── app.py              # Основное приложение Flask
├── test_app.py         # Тесты
├── build.py            # Скрипт сборки артефактов
├── requirements.txt    # Python зависимости
├── pytest.ini          # Конфигурация pytest
├── setup.py            # Установочный скрипт
├── Makefile            # Makefile с командами
├── .gitignore          # Git ignore файл
└── README.md           # Этот файл
```

## Типы генерируемых артефактов

1. **Compiled bytecode** (`dist/compiled/`) - скомпилированные .pyc файлы
2. **Documentation** (`dist/docs/`) - API документация в Markdown
3. **Build metadata** (`dist/build-info.json`) - JSON с информацией о сборке
4. **Package** (`dist/package/`) - готовый пакет для деплоя
5. **Test reports** (`test-results.xml`, `coverage.xml`) - отчеты тестирования
6. **Coverage HTML** (`htmlcov/`) - HTML отчет покрытия кода

## Лицензия

MIT
