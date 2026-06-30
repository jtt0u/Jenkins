pipeline {
    agent any

    environment {
        APP_VERSION = '1.0.0'
        ENVIRONMENT = 'development'
    }

    stages {
        stage("Build") {
            steps {
                dir('python-app') {
                    sh 'python3 -m venv .venv'
                    sh '.venv/bin/pip install -r requirements.txt'
                    sh 'APP_VERSION=$APP_VERSION BUILD_NUMBER=$BUILD_NUMBER ENVIRONMENT=$ENVIRONMENT python3 build.py'
                    echo "Build completed successfully"
                }
            }
        }

        stage("Archive Build Artifacts") {
            steps {
                archiveArtifacts artifacts: 'python-app/dist/build-info.json'
                archiveArtifacts artifacts: 'python-app/dist/BUILD-REPORT.txt'
            }
        }

        stage("Archive All Build Output") {
            steps {
                archiveArtifacts artifacts: 'python-app/dist/**/*'
            }
        }

        stage("Test") {
            steps {
                dir('python-app') {
                    sh 'ENVIRONMENT=test APP_VERSION=$APP_VERSION .venv/bin/pytest -v --cov=app --cov-report=html --cov-report=xml --junit-xml=test-results.xml'
                    echo "Tests completed"
                }
            }
        }

        stage("Archive Test Reports") {
            steps {
                archiveArtifacts artifacts: 'python-app/test-results.xml'
                archiveArtifacts artifacts: 'python-app/coverage.xml'
                archiveArtifacts artifacts: 'python-app/htmlcov/**/*'
            }
        }

        stage("Archive Multiple Types") {
            steps {
                archiveArtifacts artifacts: 'python-app/dist/package/*, python-app/dist/docs/*.md, python-app/*.xml'
            }
        }

        stage("Archive Optional Files") {
            steps {
                archiveArtifacts artifacts: 'python-app/*.log', allowEmptyArchive: true
            }
        }

        stage("Archive Package with Fingerprint") {
            steps {
                archiveArtifacts artifacts: 'python-app/dist/package/**', fingerprint: true
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'python-app/dist/package/**', fingerprint: true
            archiveArtifacts artifacts: 'python-app/dist/BUILD-REPORT.txt'
        }
        always {
            archiveArtifacts artifacts: 'python-app/*.log', allowEmptyArchive: true
            archiveArtifacts artifacts: 'python-app/dist/build-info.json', allowEmptyArchive: true
        }
        failure {
            archiveArtifacts artifacts: 'python-app/**/*.log', allowEmptyArchive: true
        }
    }
}
