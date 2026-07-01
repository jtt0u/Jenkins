pipeline {
    agent none

    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10', daysToKeepStr: '30'))
        disableConcurrentBuilds()
        durabilityHint('PERFORMANCE_OPTIMIZED')
    }

    stages {
        stage('Tests') {
            failFast true

            parallel {
                stage('Unit Tests') {
                    agent {
                        label 'linux'
                    }
                    steps {
                        sh 'make test-unit'
                    }
                }

                stage('Integration Tests') {
                    agent {
                        label 'linux'
                    }
                    steps {
                        sh 'make test-integration'
                    }
                }

                stage('Lint') {
                    agent {
                        label 'linux'
                    }
                    steps {
                        sh 'make lint'
                    }
                }
            }
        }

        stage('Build App') {
            agent {
                label 'linux'
            }
            when {
                not {
                    changeset 'docs/**'
                }
            }
            steps {
                sh 'make build'
            }
        }

        stage('Test App') {
            agent {
                label 'linux'
            }
            when {
                not {
                    changeset 'docs/**'
                }
            }
            steps {
                sh 'make test'
            }
        }

        stage('Build Docs') {
            agent {
                label 'linux'
            }
            when {
                changeset 'docs/**'
            }
            steps {
                sh 'make docs'
            }
        }

        stage('Deploy') {
            agent {
                label 'linux'
            }
            options {
                timeout(time: 5, unit: 'MINUTES')
            }
            steps {
                sh 'echo "Deploying..."'
            }
        }

        stage('Quick Checks') {
            failFast true

            parallel {
                stage('Format') {
                    agent {
                        label 'linux'
                    }
                    steps {
                        sh 'echo "Checking format..." && sleep 1'
                    }
                }

                stage('Fast Lint') {
                    agent {
                        label 'linux'
                    }
                    steps {
                        sh 'echo "Linting..." && sleep 2'
                    }
                }
            }
        }

        stage('Feedback Unit Tests') {
            agent {
                label 'linux'
            }
            steps {
                sh 'echo "Running unit tests..." && sleep 5'
            }
        }

        stage('Feedback Build') {
            agent {
                label 'linux'
            }
            steps {
                sh 'echo "Building..." && sleep 10'
            }
        }

        stage('Feedback Integration Tests') {
            agent {
                label 'linux'
            }
            options {
                timeout(time: 10, unit: 'MINUTES')
            }
            steps {
                sh 'echo "Running integration tests..." && sleep 15'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
