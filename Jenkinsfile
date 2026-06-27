// Jenkinsfile 1
// Мой первый пайплайн

pipeline {
    agent any
    stages {
        stage('Prepare') {
            steps {
                echo "Preparing workspace..."
                sh 'mkdir -p build logs temp'
                echo "Directiories created"
            }
        }

        stage('Build') {
            steps {
                echo "Building application"
                sh 'echo "Build version: 1.0.0" > build/version.txt'
                echo 'Build Completed'
            }
        }

        stage('verify') {
            steps {
                echo 'Verifying build...'
                sh 'cat build/version.txt'
                sh 'ls -la build/'
                echo 'Verification completed'
            }
        }
    }
}