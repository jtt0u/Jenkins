def customImage

pipeline {
    agent any

    environment {
        DOCKER_HUB_USERNAME = 'jtt0u'
        IMAGE_NAME = 'go-app'
        IMAGE_TAG = "1.0.${BUILD_NUMBER}"
        FULL_IMAGE_NAME = "${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"
        BUILD_TIME = ''
    }

    stages {
        stage('Prepare Build Metadata') {
            steps {
                script {
                    env.BUILD_TIME = sh(
                        script: 'date -u +"%Y-%m-%dT%H:%M:%SZ"',
                        returnStdout: true
                    ).trim()

                    echo "Image: ${env.FULL_IMAGE_NAME}"
                    echo "Build time: ${env.BUILD_TIME}"
                }
            }
        }

        stage('Build Image') {
            steps {
                script {
                    customImage = docker.build(
                        env.FULL_IMAGE_NAME,
                        "--build-arg APP_VERSION=${env.IMAGE_TAG} " +
                        "--build-arg BUILD_TIME=${env.BUILD_TIME} " +
                        "go-app"
                    )
                }
            }
        }

        stage('Test Image') {
            steps {
                script {
                    customImage.inside {
                        sh '''
                            cd /app
                            ./app &
                            sleep 2
                            wget --spider http://localhost:8080/health
                            wget -qO- http://localhost:8080/info
                        '''
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        customImage.push(env.IMAGE_TAG)
                        customImage.push('latest')
                    }
                }
            }
        }

        stage('Verify Registry') {
            steps {
                sh 'docker rmi ${FULL_IMAGE_NAME} || true'
                sh 'docker pull ${FULL_IMAGE_NAME}'
                sh 'docker images ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}'
            }
        }

        stage('Tag Additional Versions') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        customImage.push('stable')
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'docker rmi ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} || true'
            sh 'docker rmi ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest || true'
            sh 'docker rmi ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:stable || true'
            sh 'docker image prune -f'
        }
    }
}
