pipeline {
    agent any

    tools {
        nodejs 'NodeJS 20'
    }

    environment {
        APP_NAME = 'jenkins-sample-app'
        NODE_ENV = 'production'
        APP_VERSION = "1.0.${BUILD_NUMBER}"
    }

    stages {
        stage("Build") {
            steps {
                dir('app') {
                    sh 'npm install'
                    sh 'npm run build'
                    sh 'echo "Build completed for version $APP_VERSION"'
                }
            }
        }

        stage("Test with API Key") {
            steps {
                withCredentials([
                    string(credentialsId: 'api-key', variable: 'API_KEY')
                ]) {
                    dir('app') {
                        sh 'API_KEY=$API_KEY NODE_ENV=test APP_VERSION=$APP_VERSION npm test'
                        sh 'echo "API key: $API_KEY"'
                        echo "Tests completed with API key configured"
                    }
                }
            }
        }

        stage("Configure Database") {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'database-creds',
                        usernameVariable: 'DB_USER',
                        passwordVariable: 'DB_PASS'
                    )
                ]) {
                    sh 'echo "Configuring database connection..."'
                    sh 'echo "Database user: $DB_USER"'
                    sh 'echo "Database password: $DB_PASS"'
                    sh 'echo "DB_USER=$DB_USER" > app/db.config'
                    sh 'echo "DB_PASS=$DB_PASS" >> app/db.config'
                    echo "Database configuration created"
                }
            }
        }

        stage("Run Application with Secrets") {
            steps {
                withCredentials([
                    string(credentialsId: 'api-key', variable: 'API_KEY'),
                    string(credentialsId: 'database-url', variable: 'DATABASE_URL')
                ]) {
                    dir('app') {
                        sh 'echo "Starting application with all credentials configured"'
                        sh '''
                            NODE_ENV=$NODE_ENV APP_VERSION=$APP_VERSION BUILD_NUMBER=$BUILD_NUMBER API_KEY=$API_KEY DATABASE_URL=$DATABASE_URL npm start &
                            sleep 3
                            curl http://localhost:3000/config
                            pkill -f "node server.js"
                        '''
                    }
                }
            }
        }
    }
}
