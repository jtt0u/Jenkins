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

        stage("Deploy Strategy") {
            steps {
                script {
                    def strategy = input(
                        message: "Select deployment strategy",
                        parameters: [
                            choice(
                                name: 'STRATEGY',
                                choices: ['rolling', 'blue-green', 'canary'],
                                description: 'Deployment strategy'
                            )
                        ]
                    )

                    echo "Selected strategy: ${strategy}"

                    if (strategy == 'rolling') {
                        echo "Deploying with rolling update..."
                    } else if (strategy == 'blue-green') {
                        echo "Deploying with blue-green strategy..."
                    } else if (strategy == 'canary') {
                        echo "Deploying with canary release..."
                    }
                }
            }
        }

        stage("Approval with Timeout") {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    input message: "Approve within 2 minutes"
                    echo "Approval received in time"
                }
            }
        }

        stage("Advanced Approval") {
            steps {
                script {
                    def approval = input(
                        message: "Configure deployment",
                        parameters: [
                            string(
                                name: 'VERSION',
                                defaultValue: '1.0.0',
                                description: 'Application version'
                            ),
                            choice(
                                name: 'ENVIRONMENT',
                                choices: ['staging', 'production'],
                                description: 'Deployment environment'
                            ),
                            booleanParam(
                                name: 'SEND_NOTIFICATION',
                                defaultValue: true,
                                description: 'Send notification after deployment'
                            )
                        ]
                    )

                    echo "Version: ${approval.VERSION}"
                    echo "Environment: ${approval.ENVIRONMENT}"
                    echo "Send notification: ${approval.SEND_NOTIFICATION}"
                }
            }
        }
    }
}
