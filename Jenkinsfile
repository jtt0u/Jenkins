pipeline {
    agent any

    environment {
        APP_NAME = 'jenkins-sample-app'
        NODE_ENV = 'development'
        PORT = '3000'
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
    }
}
