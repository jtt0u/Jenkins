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
            steps {
                echo "Running tests..."
                sh 'sleep 2'
                echo "Tests passed"
            }
        }

        stage("Deploy to Production") {
            steps{
                input message: "Deploy to production?"
                echo "Deploying to production..."
                sh 'sleep 3'
                echo "Deployment completed successfully"
            }
        }

        stage("Notify Team") {
            steps {
                input message: "Send notification to the team?",
                ok: "Send Notification"
                echo "Sending notification..."
                echo "Notification sent to team@company.com"
            }
        }
    }
}