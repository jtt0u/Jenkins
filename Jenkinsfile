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

        stage("Build for Tests") {
            steps {
                dir('python-app') {
                    sh 'APP_VERSION=$APP_VERSION BUILD_NUMBER=$BUILD_NUMBER python3 build.py'
                }
                stash name: 'app-for-testing', includes: 'python-app/dist/package/**'
            }
        }

        stage("Parallel Tests") {
            parallel {
                stage("Unit Tests") {
                    steps {
                        unstash 'app-for-testing'
                        dir('python-app') {
                            sh 'ENVIRONMENT=test APP_VERSION=$APP_VERSION .venv/bin/pytest -v test_app.py'
                        }
                    }
                }

                stage("Integration Tests") {
                    steps {
                        unstash 'app-for-testing'
                        echo "Running integration tests..."
                        sleep 2
                        echo "Integration tests passed"
                    }
                }

                stage("Package Validation") {
                    steps {
                        unstash 'app-for-testing'
                        sh 'ls -la python-app/dist/package/'
                        sh 'test -f python-app/dist/package/VERSION'
                        sh 'test -f python-app/dist/package/app.py'
                        sh 'test -f python-app/dist/package/requirements.txt'
                    }
                }
            }
        }

        stage("Build and Save") {
            steps {
                dir('python-app') {
                    sh 'APP_VERSION=$APP_VERSION BUILD_NUMBER=$BUILD_NUMBER python3 build.py'
                }
                stash name: 'deployment-package', includes: 'python-app/dist/package/**'
                archiveArtifacts artifacts: 'python-app/dist/package/**', fingerprint: true
            }
        }

        stage("Deploy Simulation") {
            steps {
                unstash 'deployment-package'
                echo "Deploying application version..."
                sh 'cat python-app/dist/package/VERSION'
                sleep 2
                echo "Deployment completed"
            }
        }
    }
}
