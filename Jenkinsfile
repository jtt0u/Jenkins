pipeline {
    agent none

    stages {
        stage("Build Go App") {
            agent {
                docker {
                    image 'golang:1.21'
                    reuseNode true
                }
            }
            steps {
                dir('go-app') {
                    sh 'go build -o app .'
                    echo "Go application built successfully"
                }
            }
        }

        stage("Test Go App") {
            agent {
                docker {
                    image 'golang:1.21'
                    reuseNode true
                }
            }
            steps {
                dir('go-app') {
                    sh 'go test -v ./...'
                }
            }
        }

        stage("Lint") {
            agent {
                docker {
                    image 'golang:1.21'
                    reuseNode true
                }
            }
            steps {
                dir('go-app') {
                    sh 'go fmt ./...'
                    sh 'go vet ./...'
                }
            }
        }

        stage("Package Info") {
            agent {
                docker {
                    image 'alpine:latest'
                    reuseNode true
                }
            }
            steps {
                sh 'cat /etc/alpine-release'
                sh 'find . -type f | wc -l'
            }
        }

        stage("Node Info") {
            agent {
                docker {
                    image 'node:18'
                    reuseNode true
                }
            }
            steps {
                sh 'node --version'
                sh 'npm --version'
            }
        }
    }
}
