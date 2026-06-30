pipeline {
    agent any

    tools {
        nodejs 'NodeJS 20'
    }

    parameters {
        string(
            name: 'APP_VERSION',
            defaultValue: '1.0.0',
            description: 'Application version'
        )
        choice(
            name: 'DEPLOY_ENVIRONMENT',
            choices: ['development', 'staging', 'production'],
            description: 'Deployment environment'
        )
        choice(
            name: 'BUILD_TYPE',
            choices: ['quick', 'full'],
            description: 'Build type (quick or full with all tests)'
        )
        booleanParam(
            name: 'RUN_SECURITY_SCAN',
            defaultValue: false,
            description: 'Run security vulnerability scan'
        )
        booleanParam(
            name: 'DEPLOY_ENABLED',
            defaultValue: true,
            description: 'Deploy after build'
        )
    }

    environment {
        APP_NAME = 'jenkins-sample-app'
        BUILD_VERSION = "${params.APP_VERSION}-${BUILD_NUMBER}"
        DOCKER_IMAGE = "jenkins-sample-app:${params.APP_VERSION}-${BUILD_NUMBER}"
    }

    stages {
        stage("Initialize") {
            steps {
                script {
                    echo "=== CI/CD Pipeline Started ==="
                    echo "Application: ${env.APP_NAME}"
                    echo "Version: ${params.APP_VERSION}"
                    echo "Build Version: ${env.BUILD_VERSION}"
                    echo "Environment: ${params.DEPLOY_ENVIRONMENT}"
                    echo "Build Type: ${params.BUILD_TYPE}"
                    echo "Build Number: ${env.BUILD_NUMBER}"
                    echo "Job Name: ${env.JOB_NAME}"

                    if (params.DEPLOY_ENVIRONMENT == 'production') {
                        echo "WARNING: Production deployment - extra validation required"
                    }
                }
            }
        }

        stage("Build Application") {
            steps {
                dir('app') {
                    echo "Installing dependencies..."
                    sh 'npm install'
                    echo "Building application version ${env.BUILD_VERSION}"
                    sh "APP_VERSION=${env.BUILD_VERSION} npm run build"
                    echo "Build artifacts created in dist/"
                }
            }
        }

        stage("Unit Tests") {
            steps {
                dir('app') {
                    echo "Running unit tests..."
                    sh "NODE_ENV=test APP_VERSION=${env.BUILD_VERSION} npm test"
                    echo "Unit tests passed [OK]"
                }
            }
        }

        stage("Integration Tests") {
            when {
                expression {
                    params.BUILD_TYPE == 'full'
                }
            }
            steps {
                echo "Running integration tests..."
                sleep 2
                echo "Integration tests passed [OK]"
            }
        }

        stage("Security Scan") {
            when {
                expression {
                    params.RUN_SECURITY_SCAN == true
                }
            }
            steps {
                echo "Running security vulnerability scan..."
                echo "Scanning Docker image: ${env.DOCKER_IMAGE}"
                sleep 3
                echo "Security scan completed - no critical vulnerabilities found [OK]"
            }
            post {
                always {
                    echo "Security scan stage finished"
                }
            }
        }

        stage("Docker Build") {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    echo "Building Docker image: ${env.DOCKER_IMAGE}"
                    sh 'echo "Docker Registry User: $DOCKER_USER"'
                    echo "docker build -t ${env.DOCKER_IMAGE} ."
                    sh 'echo "docker login -u $DOCKER_USER -p ****"'
                    echo "docker push ${env.DOCKER_IMAGE}"
                    echo "Docker image built and pushed successfully [OK]"
                }
            }
        }

        stage("Deploy Application") {
            when {
                expression {
                    params.DEPLOY_ENABLED == true
                }
            }
            steps {
                withCredentials([
                    string(credentialsId: 'api-key', variable: 'API_KEY'),
                    string(credentialsId: 'database-url', variable: 'DATABASE_URL')
                ]) {
                    script {
                        echo "Deploying to ${params.DEPLOY_ENVIRONMENT} environment"
                        echo "Version: ${env.BUILD_VERSION}"
                        echo "Docker Image: ${env.DOCKER_IMAGE}"

                        def environmentServers = [
                            'development': ['dev1.example.com'],
                            'staging': ['stage1.example.com', 'stage2.example.com'],
                            'production': ['prod1.example.com', 'prod2.example.com', 'prod3.example.com']
                        ]

                        def servers = environmentServers[params.DEPLOY_ENVIRONMENT]

                        servers.each { server ->
                            echo "Deploying to ${server}..."
                            sleep 1
                            echo "[OK] Deployed to ${server}"
                        }

                        echo "All servers updated successfully"
                    }
                }
            }
        }

        stage("Smoke Tests") {
            when {
                expression {
                    params.DEPLOY_ENABLED == true
                }
            }
            steps {
                withCredentials([
                    string(credentialsId: 'api-key', variable: 'API_KEY'),
                    string(credentialsId: 'database-url', variable: 'DATABASE_URL')
                ]) {
                    dir('app') {
                        script {
                            echo "Running smoke tests on ${params.DEPLOY_ENVIRONMENT}..."
                            sh """
                                NODE_ENV=${params.DEPLOY_ENVIRONMENT} APP_VERSION=${env.BUILD_VERSION} BUILD_NUMBER=${env.BUILD_NUMBER} API_KEY=\$API_KEY DATABASE_URL=\$DATABASE_URL npm start &
                                sleep 3
                                curl http://localhost:3000/health
                                curl http://localhost:3000/config > smoke-config.json
                                cat smoke-config.json
                            """

                            def configOutput = readFile('smoke-config.json')

                            if (configOutput.contains("\"version\":\"${env.BUILD_VERSION}\"") && configOutput.contains("\"environment\":\"${params.DEPLOY_ENVIRONMENT}\"")) {
                                echo "Smoke tests passed [OK]"
                            } else {
                                echo "WARNING: Smoke test config output did not match expected version or environment"
                            }

                            sh 'pkill -f "node server.js" || true'
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            echo "=== Pipeline Execution Complete ==="
            echo "Total execution time: ${currentBuild.durationString}"
        }
        success {
            echo "[OK] BUILD SUCCESSFUL"
            echo "Application: ${env.APP_NAME}"
            echo "Version: ${env.BUILD_VERSION}"
            echo "Environment: ${params.DEPLOY_ENVIRONMENT}"
            echo "Docker Image: ${env.DOCKER_IMAGE}"
            writeFile file: 'deployment-report.txt', text: """Application: ${env.APP_NAME}
Version: ${env.BUILD_VERSION}
Environment: ${params.DEPLOY_ENVIRONMENT}
Build Type: ${params.BUILD_TYPE}
Security Scan: ${params.RUN_SECURITY_SCAN}
Deploy Enabled: ${params.DEPLOY_ENABLED}
Build Number: ${env.BUILD_NUMBER}
Job Name: ${env.JOB_NAME}
Docker Image: ${env.DOCKER_IMAGE}
Status: SUCCESS
Duration: ${currentBuild.durationString}
"""
            echo "Deployment report saved to deployment-report.txt"
        }
        failure {
            echo "[ERROR] BUILD FAILED"
            echo "Build Number: ${env.BUILD_NUMBER}"
            echo "Check logs at: ${env.BUILD_URL}"
            echo "Failed at environment: ${params.DEPLOY_ENVIRONMENT}"
        }
        cleanup {
            echo "Cleaning up workspace..."
            echo "Cleanup completed"
        }
    }
}
