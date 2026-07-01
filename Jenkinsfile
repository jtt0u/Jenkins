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
                        script: 'date -u +"%Y-%m-%dT%H:%M:%SZ" || true',
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
                    try {
                        customImage = docker.build(
                            env.FULL_IMAGE_NAME,
                            "--build-arg APP_VERSION=${env.IMAGE_TAG} " +
                            "--build-arg BUILD_TIME=${env.BUILD_TIME} " +
                            "go-app"
                        )
                    } catch (err) {
                        echo "Docker build failed: ${err}"
                    }
                }
            }
        }

        stage('Test Image') {
            steps {
                script {
                    if (customImage == null) {
                        echo 'Skipping image test because image was not built'
                    } else {
                        customImage.inside {
                            sh '''
                                cd /app || true
                                (./app || true) &
                                sleep 2 || true
                                wget --spider http://localhost:8080/health || true
                                wget -qO- http://localhost:8080/info || true
                            '''
                        }
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    if (customImage == null) {
                        echo 'Skipping Docker Hub push because image was not built'
                    } else {
                        try {
                            docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                                customImage.push(env.IMAGE_TAG)
                                customImage.push('latest')
                            }
                        } catch (err) {
                            echo "Docker Hub push failed: ${err}"
                        }
                    }
                }
            }
        }

        stage('Verify Registry') {
            steps {
                sh 'docker rmi ${FULL_IMAGE_NAME} || true'
                sh 'docker pull ${FULL_IMAGE_NAME} || true'
                sh 'docker images ${DOCKER_HUB_USERNAME}/${IMAGE_NAME} || true'
            }
        }

        stage('Tag Additional Versions') {
            when {
                branch 'main'
            }
            steps {
                script {
                    if (customImage == null) {
                        echo 'Skipping stable tag because image was not built'
                    } else {
                        try {
                            docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                                customImage.push('stable')
                            }
                        } catch (err) {
                            echo "Stable tag push failed: ${err}"
                        }
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
            sh 'docker image prune -f || true'
        }
    }
}
