pipeline{
    agent any
    stages {
        stage('Preparation') {
            steps {
                echo "Starting WebStore CI/CD Pipeline"
                sh 'mkdir -p build test-reports artifacts'
                sh 'date'
                echo "node: ${NODE_NAME} and Workspace: ${WORKSPACE}"
            }
        }

        stage('Generate Version') {
            steps {
                script {
                    def major = 2
                    def minor = 1
                    def patch = env.BUILD_NUMBER
                    env.APP_VERSION = "${major}.${minor}.${patch}-${env.GIT_COMMIT.take(7)}"
                    echo "Application version: ${env.APP_VERSION}"
                }
            }
        }

        stage('Build Application') {
            steps {
                script {
                    echo "Building WebStore version ${env.APP_VERSION}"
                    sh "echo '${env.APP_VERSION}' > build/version.txt"
                    sh 'echo "WebStore Application Binary" > build/app.jar'
                    sh 'ls -la build/'
                    echo "Build completed successfully"
                }
            }
        }

        stage('Unit Tests') {
            steps {
                script {
                    echo "Running unit tests..."
                    sh 'echo "Unit tests: PASSED" > test-reports/unit-tests.xml'
                    sh 'sleep 2'
                    echo "Unit tests completed"
                }
            }
        }

        stage('Integration Tests') {
            steps {
                script {
                    echo "Running integration tests..."
                    sh 'echo "Integration tests: PASSED" > test-reports/integration-tests.xml'
                    sh 'sleep 3'
                    echo "Integration tests completed"
                }
            }
        }

        stage('Package Artifacts') {
            steps {
                script {
                    def artifactName = "webstore-${env.APP_VERSION}.tar.gz"
                    echo "Creating artifact: ${artifactName}"
                    sh "tar -czf artifacts/${artifactName} build/ test-reports/"
                    sh 'ls -lh artifacts/'
                    echo "Artifact ready for deployment"
                }
            }
        }

        stage('Summary') {
            steps {
                script {
                    echo "=== Build Summary ==="
                    echo "Application: WebStore"
                    echo "Version: ${env.APP_VERSION}"
                    echo "Build Number: ${env.BUILD_NUMBER}"
                    echo "Build URL: ${env.BUILD_URL}"
                    echo "Status: SUCCESS"
                    echo "=== End of Pipeline ==="
                }
            }
        }
    }
}
