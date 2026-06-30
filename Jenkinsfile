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
                stash name: 'package-only', includes: 'python-app/dist/package/**', excludes: 'python-app/dist/package/*.pyc'
            }
        }

        stage("Verify Build") {
            steps {
                unstash 'built-app'
                sh 'ls -la python-app/dist/'
                sh 'cat python-app/dist/build-info.json'
            }
        }

        stage("Package Test") {
            steps {
                unstash 'package-only'
                sh 'ls -la python-app/dist/package/'
                sh 'find python-app/dist/package -name "*.pyc" -print -quit | grep -q . && exit 1 || echo "No .pyc files found"'
            }
        }

        stage("Build and Stash Multiple") {
            steps {
                dir('python-app') {
                    sh 'APP_VERSION=$APP_VERSION BUILD_NUMBER=$BUILD_NUMBER python3 build.py'
                }
                stash name: 'binaries', includes: 'python-app/dist/package/**'
                stash name: 'docs', includes: 'python-app/dist/docs/**'
                stash name: 'metadata', includes: 'python-app/dist/*.json, python-app/dist/*.txt'
            }
        }

        stage("Use Binaries") {
            steps {
                unstash 'binaries'
                sh 'ls -la python-app/dist/package/'
                sh 'cat python-app/dist/package/VERSION'
            }
        }

        stage("Publish Docs") {
            steps {
                unstash 'docs'
                sh 'cat python-app/dist/docs/API.md'
            }
        }

        stage("Check Metadata") {
            steps {
                unstash 'metadata'
                sh 'cat python-app/dist/build-info.json && cat python-app/dist/BUILD-REPORT.txt'
            }
        }
    }
}
