pipeline {
    agent any

    environment {
        APP_NAME = 'jenkins-sample-app'
        NODE_ENV = 'development'
        PORT = '3000'
        APP_VERSION = "1.0.${BUILD_NUMBER}"
    }

    stages {
        stage("Show Build Info") {
            steps {
                echo "Build Number: ${env.BUILD_NUMBER}"
                echo "Job Name: ${env.JOB_NAME}"
                echo "Workspace: ${env.WORKSPACE}"
                echo "Build URL: ${env.BUILD_URL}"
            }
        }

        stage("Install Dependencies") {
            steps {
                dir('app') {
                    sh 'npm install'
                    sh 'echo "Dependencies installed for $APP_NAME"'
                }
            }
        }

        stage("Build") {
            steps {
                dir('app') {
                    sh 'echo "Building $APP_NAME version $APP_VERSION"'
                    sh 'npm run build'
                    echo "Build completed successfully"
                }
            }
        }

        stage("Test") {
            environment {
                NODE_ENV = 'test'
            }
            steps {
                dir('app') {
                    sh 'echo "Running tests in $NODE_ENV environment"'
                    sh 'NODE_ENV=$NODE_ENV APP_VERSION=$APP_VERSION npm test'
                }
            }
        }

        stage("Run Application") {
            steps {
                dir('app') {
                    sh 'echo "Starting $APP_NAME on port $PORT"'
                    sh '''
                        NODE_ENV=$NODE_ENV APP_VERSION=$APP_VERSION BUILD_NUMBER=$BUILD_NUMBER PORT=$PORT npm start &
                        sleep 3
                        curl http://localhost:$PORT/
                        curl http://localhost:$PORT/config
                        pkill -f "node server.js"
                    '''
                }
            }
        }
    }
}
