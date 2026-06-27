// Jenkinsfile 1
// Мой первый пайплайн

pipeline {
    agent any
    stages {
        stage('prepare') {
            steps {
                echo "Preparing workspace..."
                sh 'mkdir -p build logs temp'
                echo "Directiories created"
            }
        }
    }
}