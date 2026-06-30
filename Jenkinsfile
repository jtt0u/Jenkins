pipeline {
    agent any

    environment {
        APP_VERSION = '1.0.0'
        ENVIRONMENT = 'production'
    }

    stages {
        stage("Build") {
            steps {
                dir('python-app') {
                    sh 'python3 -m venv .venv'
                    sh '.venv/bin/pip install -r requirements.txt'
                    sh 'APP_VERSION=$APP_VERSION BUILD_NUMBER=$BUILD_NUMBER python3 build.py'
                }
                stash name: 'built-app', includes: 'python-app/dist/**'
            }
        }

        stage("Verify Build") {
            steps {
                unstash 'built-app'
                sh 'ls -la python-app/dist/'
                sh 'cat python-app/dist/build-info.json'
            }
        }
    }
}
