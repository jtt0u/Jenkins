pipeline {
    agent any

    stages {
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
    }
}
