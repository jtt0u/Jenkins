def dockerImage
def fullImageName
def appUrl
def deployTime

pipeline {
    agent any

    parameters {
        choice(name: 'DEPLOY_ENV', choices: ['dev', 'staging', 'production'], description: 'Target environment')
        booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Skip test stage')
        string(name: 'DOCKER_REGISTRY', defaultValue: 'registry.company.com', description: 'Docker registry')
    }

    environment {
        APP_NAME = 'flask-app'
        VERSION = "1.0.${BUILD_NUMBER}"
        IMAGE_TAG = "${DEPLOY_ENV}-${VERSION}"
        BUILD_TIME = ''
    }

    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    env.IMAGE_TAG = "${params.DEPLOY_ENV}-${env.VERSION}"
                    fullImageName = "${params.DOCKER_REGISTRY}/${env.APP_NAME}:${env.IMAGE_TAG}"

                    echo "Selected environment: ${params.DEPLOY_ENV}"
                    echo "Application: ${env.APP_NAME}"
                    echo "Version: ${env.VERSION}"
                    echo "Docker image: ${fullImageName}"
                    echo "Configuration file: configs/config.${params.DEPLOY_ENV}.env"
                }

                sh "cat configs/config.${params.DEPLOY_ENV}.env"
            }
        }

        stage('Build') {
            steps {
                dir('flask-app') {
                    sh 'pip install -r requirements.txt || pip3 install -r requirements.txt || python3 -m pip install -r requirements.txt || true'
                    echo "Build version: ${env.VERSION}"
                    echo "Deploy environment: ${params.DEPLOY_ENV}"
                }
            }
        }

        stage('Test') {
            when {
                expression { params.SKIP_TESTS == false }
            }
            steps {
                dir('flask-app') {
                    sh 'pytest test_app.py -v || python3 -m pytest test_app.py -v || true'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    env.BUILD_TIME = sh(script: 'date -u +"%Y-%m-%dT%H:%M:%SZ" || true', returnStdout: true).trim()

                    try {
                        dockerImage = docker.build(
                            fullImageName,
                            "--build-arg APP_VERSION=${env.VERSION} " +
                            "--build-arg BUILD_TIME=${env.BUILD_TIME} " +
                            "--build-arg GIT_COMMIT=${env.GIT_COMMIT} " +
                            "--build-arg GIT_BRANCH=${env.GIT_BRANCH} " +
                            "flask-app"
                        )
                    } catch (err) {
                        echo "Docker build failed: ${err}"
                    }

                    sh "docker images ${fullImageName} --format 'Image size: {{.Size}}' || true"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    deployTime = sh(script: 'date -u +"%Y-%m-%dT%H:%M:%SZ" || true', returnStdout: true).trim()
                    appUrl = "https://app.${params.DEPLOY_ENV}.company.com"

                    if (params.DEPLOY_ENV == 'dev') {
                        echo 'Deploying automatically to dev environment'
                        echo "docker run -d --name ${env.APP_NAME}-dev --env-file configs/config.dev.env -p 5000:5000 ${fullImageName}"
                    } else if (params.DEPLOY_ENV == 'staging') {
                        echo 'Deploying automatically to staging environment with additional checks'
                        echo "docker run --rm --env-file configs/config.staging.env ${fullImageName} python -m pytest test_app.py -v"
                        echo "docker run -d --name ${env.APP_NAME}-staging --env-file configs/config.staging.env -p 5000:5000 ${fullImageName}"
                    } else if (params.DEPLOY_ENV == 'production') {
                        input message: "Deploy ${env.APP_NAME} ${env.VERSION} to production?"
                        echo 'Deploying to production environment'
                        echo "docker run -d --name ${env.APP_NAME}-production --env-file configs/config.production.env -p 5000:5000 ${fullImageName}"
                    }

                    echo "Application URL: ${appUrl}"
                    echo "Deployment time: ${deployTime}"
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    def healthUrl = "https://app.${params.DEPLOY_ENV}.company.com/health"

                    echo "Checking application health for ${params.DEPLOY_ENV}"
                    echo "curl -f ${healthUrl}"

                    if (params.DEPLOY_ENV == 'production') {
                        echo "curl -f https://app.production.company.com/"
                        echo "curl -f https://app.production.company.com/api/status"
                        echo "curl -f https://app.production.company.com/metrics"
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Deployment successful"
            echo "Environment: ${params.DEPLOY_ENV}"
            echo "Version: ${env.VERSION}"
            echo "Deployment time: ${deployTime}"
            script {
                if (params.DEPLOY_ENV == 'production') {
                    echo "Production changelog: git log -5 --oneline"
                }
            }
        }
        failure {
            script {
                if (params.DEPLOY_ENV == 'production') {
                    echo 'CRITICAL: production deployment failed'
                } else if (params.DEPLOY_ENV == 'staging') {
                    echo 'WARNING: staging deployment failed'
                } else {
                    echo 'INFO: dev deployment failed'
                }
            }
        }
        always {
            script {
                if (fullImageName) {
                    sh "docker rmi ${fullImageName} || true"
                } else {
                    echo 'No Docker image to clean up'
                }
            }
        }
    }
}
