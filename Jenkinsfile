pipeline {
    agent any

    tools {
        nodejs 'NodeJS 20'
    }

    parameters {
        string(
            name: 'APP_VERSION',
            defaultValue: '1.0.0',
            description: 'Application version to build'
        )
        choice(
            name: 'ENVIRONMENT',
            choices: ['development', 'staging', 'production'],
            description: 'Target environment'
        )
        booleanParam(
            name: 'RUN_TESTS',
            defaultValue: true,
            description: 'Run test suite'
        )
        booleanParam(
            name: 'RUN_LINT',
            defaultValue: false,
            description: 'Run linter'
        )
    }

    environment {
        APP_NAME = 'jenkins-sample-app'
        NODE_ENV = 'production'
    }

    stages {
        stage("Build") {
            steps {
                echo "Building ${env.APP_NAME} version ${params.APP_VERSION}"
                dir('app') {
                    sh 'npm install'
                    sh "APP_VERSION=${params.APP_VERSION} npm run build"
                }
                echo "Build completed for version ${params.APP_VERSION}"
            }
        }

        stage("Configure Environment") {
            steps {
                script {
                    echo "Configuring for ${params.ENVIRONMENT} environment"

                    if (params.ENVIRONMENT == 'production') {
                        echo "Production mode - strict checks enabled"
                    } else if (params.ENVIRONMENT == 'staging') {
                        echo "Staging mode - moderate checks"
                    } else {
                        echo "Development mode - minimal checks"
                    }
                }
            }
        }

        stage("Lint") {
            when {
                expression {
                    params.RUN_LINT == true
                }
            }
            steps {
                dir('app') {
                    echo "Running linter..."
                    sh 'npm run lint'
                    echo "Linting completed"
                }
            }
        }

        stage("Test") {
            when {
                expression {
                    params.RUN_TESTS == true
                }
            }
            steps {
                dir('app') {
                    echo "Running tests for ${params.APP_VERSION}"
                    sh "NODE_ENV=test APP_VERSION=${params.APP_VERSION} npm test"
                    echo "All tests passed"
                }
            }
        }

        stage("Run Application") {
            steps {
                withCredentials([
                    string(credentialsId: 'api-key', variable: 'API_KEY'),
                    string(credentialsId: 'database-url', variable: 'DATABASE_URL')
                ]) {
                    dir('app') {
                        echo "Starting application:"
                        echo "- Version: ${params.APP_VERSION}"
                        echo "- Environment: ${params.ENVIRONMENT}"
                        sh """
                            NODE_ENV=${params.ENVIRONMENT} APP_VERSION=${params.APP_VERSION} BUILD_NUMBER=\$BUILD_NUMBER API_KEY=\$API_KEY DATABASE_URL=\$DATABASE_URL npm start &
                            sleep 3
                            curl http://localhost:3000/
                            curl http://localhost:3000/config
                            pkill -f "node server.js"
                        """
                    }
                }
            }
        }
    }
}
