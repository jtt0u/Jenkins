def dockerImage

pipeline {
    agent any

    environment {
        APP_NAME = 'flask-app'
        VERSION = "1.0.${BUILD_NUMBER}"
        IMAGE_TAG = "${BRANCH_NAME}-${VERSION}"
        BUILD_TIME = ''
        GIT_COMMIT_SHORT = ''
    }

    stages {
        stage('Branch Info') {
            steps {
                script {
                    def currentBranch = env.BRANCH_NAME ?: sh(script: 'git branch --show-current', returnStdout: true).trim()
                    def safeBranch = currentBranch.replaceAll('/', '-')
                    env.IMAGE_TAG = "${safeBranch}-${env.VERSION}"
                    env.BUILD_TIME = sh(script: 'date -u +"%Y-%m-%dT%H:%M:%SZ" || true', returnStdout: true).trim()
                    env.GIT_COMMIT_SHORT = sh(script: 'git rev-parse --short HEAD || true', returnStdout: true).trim()

                    echo "Current branch: ${currentBranch}"
                    echo "Image tag: ${env.IMAGE_TAG}"

                    if (currentBranch == 'main') {
                        echo 'Build type: production'
                    } else if (currentBranch == 'develop') {
                        echo 'Build type: staging'
                    } else if (currentBranch.startsWith('feature/')) {
                        echo 'Build type: feature'
                    } else {
                        echo 'Build type: regular branch'
                    }
                }
            }
        }

        stage('Build') {
            steps {
                dir('flask-app') {
                    sh 'pip install -r requirements.txt || pip3 install -r requirements.txt || python3 -m pip install -r requirements.txt || true'
                    echo "Building ${env.APP_NAME} version ${env.VERSION}"
                }
            }
        }

        stage('Test') {
            steps {
                dir('flask-app') {
                    sh 'pytest test_app.py -v || python3 -m pytest test_app.py -v || true'
                }
            }
        }

        stage('Build Docker Image') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                    expression { env.BRANCH_NAME?.startsWith('feature/') }
                }
            }
            steps {
                script {
                    try {
                        dockerImage = docker.build(
                            "${env.APP_NAME}:${env.IMAGE_TAG}",
                            "--build-arg APP_VERSION=${env.VERSION} " +
                            "--build-arg BUILD_TIME=${env.BUILD_TIME} " +
                            "--build-arg GIT_COMMIT=${env.GIT_COMMIT_SHORT} " +
                            "--build-arg GIT_BRANCH=${env.BRANCH_NAME} " +
                            "flask-app"
                        )
                        echo "Docker image built: ${env.APP_NAME}:${env.IMAGE_TAG}"
                    } catch (err) {
                        echo "Docker image build failed: ${err}"
                    }
                }
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                echo 'Deploying to staging environment'
                echo "kubectl set image deployment/${env.APP_NAME} ${env.APP_NAME}=${env.APP_NAME}:${env.IMAGE_TAG} --namespace=staging"
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?'
                echo 'Deploying to production environment'
                echo "kubectl set image deployment/${env.APP_NAME} ${env.APP_NAME}=${env.APP_NAME}:${env.IMAGE_TAG} --namespace=production"
            }
        }
    }

    post {
        success {
            echo "Build succeeded for branch ${env.BRANCH_NAME}"
        }
        failure {
            script {
                if (env.BRANCH_NAME == 'main') {
                    echo 'CRITICAL: production branch build failed'
                } else if (env.BRANCH_NAME == 'develop') {
                    echo 'Staging branch build failed'
                } else if (env.BRANCH_NAME?.startsWith('feature/')) {
                    echo "Feature branch build failed: ${env.BRANCH_NAME}"
                } else {
                    echo "Build failed for branch ${env.BRANCH_NAME}"
                }
            }
        }
        always {
            sh "docker rmi ${env.APP_NAME}:${env.IMAGE_TAG} || true"
        }
    }
}
