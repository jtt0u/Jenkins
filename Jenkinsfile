pipeline {
    agent any

    parameters {
        choice(name: 'DEPLOY_ENVIRONMENT', choices: ['staging', 'production'], description: 'Target deployment environment')
        booleanParam(name: 'RUN_SECURITY_SCAN', defaultValue: true, description: 'Run security vulnerability scan')
    }

    environment {
        PROJECT_NAME = 'CloudStore'
        DEPLOY_ENVIRONMENT = "${params.DEPLOY_ENVIRONMENT}"
        RUN_SECURITY_SCAN = "${params.RUN_SECURITY_SCAN}"
        DEPLOY_STRATEGY = 'rolling'
    }

    stages {
        stage("Initialization") {
            steps {
                script {
                    echo "Starting ${env.PROJECT_NAME} Pipeline"

                    def services = ['auth-service', 'api-gateway', 'user-service', 'payment-service']
                    env.SERVICES = services.join(',')

                    echo "Services to build: ${env.SERVICES}"
                }
            }
        }

        stage("Build Services") {
            steps {
                script {
                    def services = env.SERVICES.split(',')

                    services.each { service ->
                        echo "Building ${service}..."
                        sh "mkdir -p build/${service}"
                        sh "touch build/${service}/app.jar"
                        sleep 1
                        echo "Build completed for ${service}"
                    }
                }
            }
        }

        stage("Unit Tests") {
            when {
                expression {
                    return env.BUILD_NUMBER.toInteger() % 2 != 0
                }
            }
            steps {
                echo "Running unit tests for build ${env.BUILD_NUMBER}"
                sleep 2
                echo "Unit tests passed"
            }
        }

        stage("Integration Tests") {
            when {
                expression {
                    return env.BUILD_NUMBER.toInteger() % 2 == 0
                }
            }
            steps {
                echo "Running integration tests for build ${env.BUILD_NUMBER}"
                sleep 2
                echo "Integration tests passed"
            }
        }

        stage("Security Scan") {
            when {
                environment name: 'RUN_SECURITY_SCAN', value: 'true'
            }
            steps {
                echo "Running security vulnerability scan..."
                sleep 3
                echo "Security scan completed - no vulnerabilities found"
            }
            post {
                always {
                    echo "Security scan stage finished"
                }
            }
        }

        stage("Deployment Approval") {
            when {
                anyOf {
                    environment name: 'DEPLOY_ENVIRONMENT', value: 'production'
                    environment name: 'DEPLOY_ENVIRONMENT', value: 'staging'
                }
            }
            steps {
                script {
                    timeout(time: 5, unit: 'MINUTES') {
                        def approval = input(
                            message: "Approve deployment to ${env.DEPLOY_ENVIRONMENT}?",
                            parameters: [
                                choice(
                                    name: 'DEPLOY_STRATEGY',
                                    choices: ['rolling', 'blue-green', 'canary'],
                                    description: 'Deployment strategy'
                                ),
                                booleanParam(
                                    name: 'SEND_NOTIFICATIONS',
                                    defaultValue: true,
                                    description: 'Send deployment notifications'
                                )
                            ]
                        )

                        echo "Selected strategy: ${approval.DEPLOY_STRATEGY}"
                        echo "Send notifications: ${approval.SEND_NOTIFICATIONS}"

                        env.DEPLOY_STRATEGY = approval.DEPLOY_STRATEGY
                    }
                }
            }
        }

        stage("Deploy Services") {
            steps {
                script {
                    def environmentServers = [
                        'staging': ['stage1.example.com', 'stage2.example.com'],
                        'production': ['prod1.example.com', 'prod2.example.com', 'prod3.example.com']
                    ]

                    def servers = environmentServers[env.DEPLOY_ENVIRONMENT]
                    def services = env.SERVICES.split(',')

                    servers.each { server ->
                        services.each { service ->
                            echo "Deploying ${service} to ${server} using ${env.DEPLOY_STRATEGY} strategy"
                            sleep 1
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            echo "=== Pipeline Execution Complete ==="
            echo "Total build time: ${currentBuild.durationString}"
        }
        success {
            echo "✓ Deployment SUCCESS"
            echo "Project: ${env.PROJECT_NAME}"
            echo "Environment: ${env.DEPLOY_ENVIRONMENT}"
            echo "All services deployed successfully"
            writeFile file: 'deployment-report.txt', text: """Project: ${env.PROJECT_NAME}
Environment: ${env.DEPLOY_ENVIRONMENT}
Build Number: ${env.BUILD_NUMBER}
Deploy Strategy: ${env.DEPLOY_STRATEGY}
Services: ${env.SERVICES}
Status: SUCCESS
Duration: ${currentBuild.durationString}
"""
        }
        failure {
            echo "✗ Deployment FAILED"
            echo "Build Number: ${env.BUILD_NUMBER}"
            echo "Check logs at: ${env.BUILD_URL}"
            echo "Rolling back changes..."
        }
        cleanup {
            echo "Cleaning up temporary files..."
            echo "Cleanup completed"
        }
    }
}
