pipeline {
    agent any

    options {
        skipDefaultCheckout()
    }

    stages {
        stage("Full Clean") {
            steps {
                deleteDir()
                echo "Workspace cleaned completely"
            }
        }

        stage("Checkout Code") {
            steps {
                checkout scm
                echo "Code checked out"
            }
        }

        stage("Inspect Workspace") {
            steps {
                sh 'pwd'
                sh 'ls -la'
                sh 'du -sh .'
                sh 'echo "Workspace: $WORKSPACE"'
            }
        }

        stage("Create Test Files") {
            steps {
                sh 'echo "test" > test1.txt'
                sh 'mkdir -p temp && echo "temp" > temp/temp.log'
                sh 'mkdir -p old-build && echo "old" > old-build/app.jar'
                sh 'ls -la'
                sh 'find temp old-build -type f -print'
            }
        }

        stage("Selective Clean") {
            steps {
                sh 'rm -rf temp/ old-build/ *.log'
                echo "Cleaned temporary files and old builds"
                sh 'ls -la'
            }
        }

        stage("Build with Selective Clean") {
            steps {
                sh 'rm -rf python-app/dist/ python-app/build/'
                sh 'mkdir -p python-app/dist'
                dir('python-app') {
                    sh 'python3 -m venv .venv'
                    sh '.venv/bin/pip install -r requirements.txt'
                    sh 'APP_VERSION=1.0.0 BUILD_NUMBER=$BUILD_NUMBER ENVIRONMENT=development python3 build.py'
                }
            }
        }

        stage("Build from Clean State") {
            steps {
                dir('python-app') {
                    sh 'python3 -m venv .venv'
                    sh '.venv/bin/pip install -r requirements.txt'
                    sh 'python3 build.py'
                }
            }
        }

        stage("Build and Test") {
            steps {
                dir('python-app') {
                    sh 'python3 -m venv .venv'
                    sh '.venv/bin/pip install -r requirements.txt'
                    sh 'APP_VERSION=1.0.0 BUILD_NUMBER=$BUILD_NUMBER ENVIRONMENT=development python3 build.py'
                    sh 'ENVIRONMENT=test APP_VERSION=1.0.0 .venv/bin/pytest -v test_app.py'
                }
                archiveArtifacts artifacts: 'python-app/dist/**'
            }
        }
    }

    post {
        always {
            sh 'du -sh .'
            cleanWs(
                deleteDirs: true,
                patterns: [
                    [pattern: 'python-app/dist/compiled/**', type: 'INCLUDE'],
                    [pattern: 'python-app/__pycache__/**', type: 'INCLUDE'],
                    [pattern: 'python-app/*.pyc', type: 'INCLUDE'],
                    [pattern: 'python-app/dist/package/**', type: 'EXCLUDE'],
                    [pattern: '.git/**', type: 'EXCLUDE']
                ]
            )
            echo "Workspace cleaned after build"
        }
    }
}
