def call(Map config = [:]) {
    if (!config.service) {
        error 'Parameter "service" is required'
    }

    def service = config.service
    def testCommand = config.testCommand ?: 'make test'
    def dockerfilePath = config.dockerfilePath ?: 'Dockerfile'

    pipeline {
        agent any

        stages {
            stage('Test') {
                steps {
                    sh testCommand
                }
            }

            stage('Build') {
                steps {
                    script {
                        buildImage(image: service, dockerfile: dockerfilePath)
                    }
                }
            }

            stage('Deploy') {
                steps {
                    echo "Deploying ${service} to staging"
                }
            }
        }

        post {
            always {
                echo "Pipeline for ${service} finished"
            }
        }
    }
}
