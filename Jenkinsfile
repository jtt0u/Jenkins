@Library('my-shared-lib') _

def effectiveImageTag
def builtImage

pipeline {
    agent any

    parameters {
        choice(name: 'DEPLOY_ENV', choices: ['staging', 'production'], description: 'Target environment')
        booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Skip test stage')
        string(name: 'IMAGE_TAG', defaultValue: '', description: 'Docker image tag. If empty, BUILD_NUMBER is used')
    }

    environment {
        SERVICE_NAME = 'web-app'
        DOCKER_REGISTRY = 'docker.io/jtt0u'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare') {
            steps {
                script {
                    effectiveImageTag = params.IMAGE_TAG?.trim() ? params.IMAGE_TAG.trim() : env.BUILD_NUMBER
                    currentBuild.description = "${params.DEPLOY_ENV} / ${effectiveImageTag}"
                }

                echo "Service: ${env.SERVICE_NAME}"
                echo "Deploy environment: ${params.DEPLOY_ENV}"
                echo "Docker registry: ${env.DOCKER_REGISTRY}"
                echo "Image tag: ${effectiveImageTag}"
                sh 'docker --version || true'
                sh 'kubectl version --client || true'
            }
        }

        stage('Quality Checks') {
            failFast true

            parallel {
                stage('Lint') {
                    steps {
                        sh 'echo "Running linter..." && sleep 3'
                    }
                }

                stage('Security Scan') {
                    steps {
                        sh 'echo "Running security scan..." && sleep 2'
                    }
                }
            }
        }

        stage('Test') {
            when {
                expression { params.SKIP_TESTS == false }
            }
            steps {
                sh 'echo "Running tests..." && sleep 5'
            }
        }

        stage('Build') {
            steps {
                script {
                    builtImage = buildDocker(
                        image: env.SERVICE_NAME,
                        tag: effectiveImageTag,
                        dockerfile: 'Dockerfile',
                        registry: env.DOCKER_REGISTRY,
                        push: false
                    )
                    echo "Built image: ${builtImage}"
                }
            }
        }

        stage('Deploy to Staging') {
            when {
                anyOf {
                    expression { params.DEPLOY_ENV == 'staging' }
                    expression { params.DEPLOY_ENV == 'production' }
                }
            }
            steps {
                script {
                    deployApp(
                        app: env.SERVICE_NAME,
                        image: builtImage,
                        env: 'staging',
                        replicas: 1
                    )
                }
            }
        }

        stage('Deploy to Production') {
            when {
                expression { params.DEPLOY_ENV == 'production' }
            }
            steps {
                input message: 'Deploy to production?'
                script {
                    deployApp(
                        app: env.SERVICE_NAME,
                        image: builtImage,
                        env: 'production',
                        replicas: 3
                    )
                }
            }
        }
    }

    post {
        success {
            notifyBuild(status: 'SUCCESS', service: env.SERVICE_NAME)
        }
        failure {
            notifyBuild(status: 'FAILURE', service: env.SERVICE_NAME)
        }
        always {
            echo 'Pipeline finished'
            cleanWs()
        }
    }
}
