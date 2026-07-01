@Library('my-shared-lib@v1.0.0') _

def builtImage

pipeline {
    agent any

    stages {
        stage('Greet') {
            steps {
                sayHello(name: 'Jenkins')
            }
        }

        stage('Build') {
            steps {
                script {
                    builtImage = buildImage(image: 'my-web-app', tag: 'latest')
                    echo "Built image: ${builtImage}"
                }
            }
        }

        stage('Config') {
            steps {
                generateConfig(app: 'my-web-app', version: 'latest', env: 'staging')
            }
        }
    }
}
