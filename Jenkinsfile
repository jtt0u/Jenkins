pipeline {
    agent any
    stages {
        stage("Build") {
            steps {
                echo "Building application..."
                sh 'sleep 2 для'
                echo "Build completed"
            }
        }

        stage("Test") {
            echo "Running tests..."
            sh 'sleep 2'
            echo "Tests passed"
        }

        stage("Deploy to Production") {
            input message: "Deploy to production?"
            echo "Deploying to production..."
            sh 'sleep 3'
            echo "Deployment completed successfully"
        }
    }
}