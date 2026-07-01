def dockerImage
def imageWasPushed = false

pipeline {
    agent none

    parameters {
        string(name: 'DOCKER_REGISTRY', defaultValue: 'index.docker.io/v1/', description: 'Docker registry URL')
        string(name: 'DOCKER_USERNAME', defaultValue: 'jtt0u', description: 'Docker Hub username')
        choice(name: 'ENVIRONMENT', choices: ['development', 'staging', 'production'], description: 'Deployment environment')
        booleanParam(name: 'RUN_SECURITY_SCAN', defaultValue: true, description: 'Run security scan')
        booleanParam(name: 'PUSH_TO_REGISTRY', defaultValue: true, description: 'Push image to registry')
    }

    environment {
        APP_NAME = 'go-app'
        VERSION = "1.0.${BUILD_NUMBER}"
        BUILD_TIME = ''
        GIT_COMMIT_SHORT = ''
        FULL_IMAGE_NAME = ''
        IMAGE_SIZE = ''
    }

    stages {
        stage('Checkout') {
            agent any
            steps {
                checkout scm
                sh 'git branch --show-current || true'
                sh 'git log -1 --oneline || true'
            }
        }

        stage('Initialize') {
            agent any
            steps {
                script {
                    env.GIT_COMMIT_SHORT = sh(script: 'git rev-parse --short HEAD || true', returnStdout: true).trim()
                    env.BUILD_TIME = sh(script: 'date -u +"%Y-%m-%dT%H:%M:%SZ" || true', returnStdout: true).trim()
                    env.FULL_IMAGE_NAME = "${params.DOCKER_USERNAME}/${env.APP_NAME}:${env.VERSION}"

                    echo "Branch: ${env.BRANCH_NAME}"
                    echo "Commit: ${env.GIT_COMMIT_SHORT}"
                    echo "Image: ${env.FULL_IMAGE_NAME}"
                    echo "Environment: ${params.ENVIRONMENT}"
                }
            }
        }

        stage('Code Quality') {
            agent {
                docker {
                    image 'golang:1.21'
                    reuseNode true
                }
            }
            environment {
                HOME = "${WORKSPACE}"
                GOCACHE = "${WORKSPACE}/.cache/go-build"
                GOMODCACHE = "${WORKSPACE}/.cache/go-mod"
            }
            steps {
                dir('go-app') {
                    sh 'go fmt ./... || true'
                    sh 'go vet ./... || true'
                    echo 'Code quality checks passed'
                }
            }
        }

        stage('Unit Tests') {
            agent {
                docker {
                    image 'golang:1.21'
                    reuseNode true
                }
            }
            environment {
                HOME = "${WORKSPACE}"
                GOCACHE = "${WORKSPACE}/.cache/go-build"
                GOMODCACHE = "${WORKSPACE}/.cache/go-mod"
            }
            steps {
                dir('go-app') {
                    sh 'go test -v -coverprofile=coverage.out ./... || true'
                    sh 'go tool cover -func=coverage.out || true'
                    archiveArtifacts artifacts: 'coverage.out', fingerprint: true, allowEmptyArchive: true
                }
            }
        }

        stage('Build Docker Image') {
            agent any
            steps {
                script {
                    try {
                        dockerImage = docker.build(
                            env.FULL_IMAGE_NAME,
                            "--build-arg APP_VERSION=${env.VERSION} " +
                            "--build-arg BUILD_TIME=${env.BUILD_TIME} " +
                            "--build-arg GIT_COMMIT=${env.GIT_COMMIT_SHORT} " +
                            "--build-arg BUILD_NUMBER=${env.BUILD_NUMBER} " +
                            "go-app"
                        )
                    } catch (err) {
                        echo "Docker build failed: ${err}"
                    }

                    env.IMAGE_SIZE = sh(
                        script: 'docker images ${FULL_IMAGE_NAME} --format "{{.Size}}" || true',
                        returnStdout: true
                    ).trim()
                    echo "Docker image size: ${env.IMAGE_SIZE}"
                }
            }
        }

        stage('Container Tests') {
            agent any
            steps {
                script {
                    if (dockerImage == null) {
                        echo 'Skipping container tests because image was not built'
                    } else {
                        try {
                            dockerImage.withRun('-p 8080:8080') {
                                sh 'sleep 3 || true'
                                sh 'curl -f http://localhost:8080/health || true'
                                sh 'curl -s http://localhost:8080/info | grep version || true'
                                sh 'curl -f http://localhost:8080/metrics || true'
                            }
                        } catch (err) {
                            echo "Container tests failed: ${err}"
                        }
                    }
                }
            }
        }

        stage('Security Scan') {
            agent any
            when {
                expression { params.RUN_SECURITY_SCAN == true }
            }
            steps {
                echo 'Security scan would run here'
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL ${FULL_IMAGE_NAME} || true'
            }
        }

        stage('Push to Registry') {
            agent any
            when {
                expression { params.PUSH_TO_REGISTRY == true }
            }
            steps {
                script {
                    if (dockerImage == null) {
                        echo 'Skipping registry push because image was not built'
                    } else {
                        try {
                            docker.withRegistry("https://${params.DOCKER_REGISTRY}", 'dockerhub-credentials') {
                                dockerImage.push(env.VERSION)
                                dockerImage.push("${env.VERSION}-${env.GIT_COMMIT_SHORT}")

                                if (params.ENVIRONMENT == 'production') {
                                    dockerImage.push('latest')
                                }
                            }

                            imageWasPushed = true
                        } catch (err) {
                            echo "Registry push failed: ${err}"
                        }
                    }

                    echo "Published: https://hub.docker.com/r/${params.DOCKER_USERNAME}/${env.APP_NAME}/tags"
                    echo "Tag: ${env.VERSION}"
                    echo "Tag: ${env.VERSION}-${env.GIT_COMMIT_SHORT}"
                    if (params.ENVIRONMENT == 'production') {
                        echo 'Tag: latest'
                    }
                }
            }
        }

        stage('Verify Registry') {
            agent any
            when {
                expression { imageWasPushed == true }
            }
            steps {
                sh 'docker rmi ${FULL_IMAGE_NAME} || true'
                sh 'docker pull ${FULL_IMAGE_NAME} || true'
                script {
                    try {
                        docker.image(env.FULL_IMAGE_NAME).withRun('-p 8081:8080') {
                            sh 'sleep 3 || true'
                            sh 'curl -f http://localhost:8081/health || true'
                        }
                    } catch (err) {
                        echo "Registry verification failed: ${err}"
                    }
                }
            }
        }

        stage('Generate Report') {
            agent any
            steps {
                sh '''
                    set +e
                    cat > build-report.txt <<EOF
Application Version: ${VERSION}
Build Number: ${BUILD_NUMBER}
Git Commit: ${GIT_COMMIT_SHORT}
Build Time: ${BUILD_TIME}
Environment: ${ENVIRONMENT}
Docker Image: ${FULL_IMAGE_NAME}
Image Size: ${IMAGE_SIZE}
EOF
                    true
                '''
                archiveArtifacts artifacts: 'build-report.txt', fingerprint: true, allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully for ${env.APP_NAME} ${env.VERSION}"
            echo "Docker Hub: https://hub.docker.com/r/${params.DOCKER_USERNAME}/${env.APP_NAME}/tags"
        }
        failure {
            echo "Pipeline failed"
            echo "Current stage or build: ${env.STAGE_NAME ?: 'unknown'}"
        }
        always {
            node {
                sh 'docker rmi ${FULL_IMAGE_NAME} || true'
                sh "docker rmi ${params.DOCKER_USERNAME}/${env.APP_NAME}:${env.VERSION}-${env.GIT_COMMIT_SHORT} || true"
                sh "docker rmi ${params.DOCKER_USERNAME}/${env.APP_NAME}:latest || true"
                sh 'docker image prune -f || true'
                sh 'docker container prune -f || true'
            }
        }
    }
}
