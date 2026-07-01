def customImage

pipeline {
    agent any

    environment {
        APP_VERSION = "1.0.${BUILD_NUMBER}"
        BUILD_TIME = ''
        GIT_COMMIT = ''
    }

    stages {
        stage('Prepare Build Metadata') {
            steps {
                script {
                    env.BUILD_TIME = sh(
                        script: 'date -u +"%Y-%m-%dT%H:%M:%SZ"',
                        returnStdout: true
                    ).trim()
                    env.GIT_COMMIT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()

                    echo "App version: ${env.APP_VERSION}"
                    echo "Build time: ${env.BUILD_TIME}"
                    echo "Git commit: ${env.GIT_COMMIT}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    customImage = docker.build(
                        "go-app:${env.BUILD_NUMBER}",
                        "--build-arg APP_VERSION=${env.APP_VERSION} " +
                        "--build-arg BUILD_TIME=${env.BUILD_TIME} " +
                        "--build-arg GIT_COMMIT=${env.GIT_COMMIT} " +
                        "go-app"
                    )

                    echo "Docker image go-app:${env.BUILD_NUMBER} built successfully"
                }
            }
        }

        stage('Test in Container') {
            steps {
                script {
                    customImage.inside {
                        sh 'ls -lh /app/app'
                        sh '''
                            cd /app
                            ./app &
                            sleep 2
                            wget -O- http://localhost:8080/health
                        '''
                    }
                }
            }
        }

        stage('Image Info') {
            steps {
                echo 'Docker image size:'
                sh 'docker images go-app:${BUILD_NUMBER} --format "{{.Size}}"'

                echo 'Docker image ID:'
                sh 'docker images go-app:${BUILD_NUMBER} --format "{{.ID}}"'

                echo 'Docker image created at:'
                sh 'docker images go-app:${BUILD_NUMBER} --format "{{.CreatedAt}}"'
            }
        }
    }

    post {
        always {
            sh 'docker rmi go-app:${BUILD_NUMBER} || true'
            sh 'docker image prune -f'
        }
    }
}
