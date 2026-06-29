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
    }
}
