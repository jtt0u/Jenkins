pipeline {
    agent any

    options {
        skipDefaultCheckout()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    parameters {
        string(
            name: 'APP_VERSION',
            defaultValue: '1.0.0',
            description: 'Application version'
        )
        choice(
            name: 'BUILD_TYPE',
            choices: ['clean', 'incremental'],
            description: 'Build cleanup strategy'
        )
        booleanParam(
            name: 'RUN_PARALLEL_TESTS',
            defaultValue: true,
            description: 'Run tests in parallel'
        )
    }

    environment {
        BUILD_VERSION = "${params.APP_VERSION}-${BUILD_NUMBER}"
        ENVIRONMENT = 'production'
    }

    stages {
        stage("Workspace Preparation") {
            steps {
                script {
                    echo "Preparing workspace..."
                    sh 'du -sh . 2>/dev/null || echo "Empty workspace"'

                    if (params.BUILD_TYPE == 'clean') {
                        deleteDir()
                    } else {
                        sh 'rm -rf python-app/dist/ python-app/build/ python-app/__pycache__/'
                    }

                    echo "Workspace prepared"
                }
            }
        }

        stage("Checkout") {
            steps {
                checkout scm
                echo "Code checked out successfully"
            }
        }

        stage("Install Dependencies") {
            steps {
                dir('python-app') {
                    sh 'test -f requirements.txt'
                    sh 'if [ ! -d ".venv" ]; then python3 -m venv .venv; fi'
                    sh '.venv/bin/pip install -r requirements.txt'
                    echo "Dependencies installed"
                }
            }
        }

        stage("Build Application") {
            steps {
                dir('python-app') {
                    echo "Building version ${env.BUILD_VERSION}"
                    sh 'APP_VERSION=$BUILD_VERSION BUILD_NUMBER=$BUILD_NUMBER ENVIRONMENT=$ENVIRONMENT .venv/bin/python build.py'
                    sh 'ls -la dist/'
                }
            }
        }

        stage("Create Stashes") {
            steps {
                stash name: 'application-package', includes: 'python-app/dist/package/**'
                stash name: 'test-files', includes: 'python-app/test_app.py, python-app/app.py, python-app/requirements.txt'
                stash name: 'documentation', includes: 'python-app/dist/docs/**, python-app/dist/*.md'
                echo "Created stashes for downstream stages"
            }
        }

        stage("Parallel Testing") {
            when {
                expression {
                    params.RUN_PARALLEL_TESTS == true
                }
            }
            parallel {
                stage("Unit Tests") {
                    steps {
                        dir('unit-workspace') {
                            unstash 'test-files'
                            dir('python-app') {
                                sh 'python3 -m venv .venv'
                                sh '.venv/bin/pip install -r requirements.txt'
                                sh 'ENVIRONMENT=test APP_VERSION=$BUILD_VERSION .venv/bin/pytest -v --junit-xml=unit-test-results.xml'
                            }
                            stash name: 'unit-test-results', includes: 'python-app/unit-test-results.xml'
                        }
                    }
                }

                stage("Coverage Tests") {
                    steps {
                        dir('coverage-workspace') {
                            unstash 'test-files'
                            dir('python-app') {
                                sh 'python3 -m venv .venv'
                                sh '.venv/bin/pip install -r requirements.txt'
                                sh 'ENVIRONMENT=test APP_VERSION=$BUILD_VERSION .venv/bin/pytest --cov=app --cov-report=html --cov-report=xml'
                            }
                            stash name: 'coverage-reports', includes: 'python-app/htmlcov/**, python-app/coverage.xml'
                        }
                    }
                }

                stage("Package Validation") {
                    steps {
                        dir('package-workspace') {
                            unstash 'application-package'
                            sh 'test -f python-app/dist/package/VERSION'
                            sh 'test -f python-app/dist/package/app.py'
                            sh 'test -f python-app/dist/package/requirements.txt'
                            sh 'cat python-app/dist/package/VERSION'
                            echo "Package validation passed"
                        }
                    }
                }
            }
        }

        stage("Collect Test Results") {
            when {
                expression {
                    params.RUN_PARALLEL_TESTS == true
                }
            }
            steps {
                unstash 'unit-test-results'
                unstash 'coverage-reports'
                echo "Test results collected"
            }
        }

        stage("Generate Reports") {
            steps {
                echo "=== Build Summary ==="
                echo "Version: ${env.BUILD_VERSION}"
                echo "Build Number: ${env.BUILD_NUMBER}"
                writeFile file: 'final-report.txt', text: """Build Summary
Version: ${env.BUILD_VERSION}
Build Number: ${env.BUILD_NUMBER}
Build Type: ${params.BUILD_TYPE}
Parallel Tests: ${params.RUN_PARALLEL_TESTS}
Environment: ${env.ENVIRONMENT}
Job: ${env.JOB_NAME}
Workspace: ${env.WORKSPACE}
"""
            }
        }

        stage("Archive All Artifacts") {
            steps {
                unstash 'application-package'
                unstash 'documentation'
                archiveArtifacts artifacts: 'python-app/dist/package/**', fingerprint: true
                archiveArtifacts artifacts: 'python-app/dist/docs/**', fingerprint: true
                archiveArtifacts artifacts: 'python-app/dist/*.json, python-app/dist/*.txt', fingerprint: true
                archiveArtifacts artifacts: 'python-app/*-test-results.xml, python-app/coverage.xml', allowEmptyArchive: true
                archiveArtifacts artifacts: 'python-app/htmlcov/**', allowEmptyArchive: true
                archiveArtifacts artifacts: 'final-report.txt'
            }
        }

        stage("Deploy to Staging") {
            when {
                expression {
                    env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'master'
                }
            }
            steps {
                unstash 'application-package'
                echo "Deploying version ${env.BUILD_VERSION} to staging..."
                sh 'ls -la python-app/dist/package/'
                sleep 2
                echo "Deployment to staging completed"
            }
        }
    }

    post {
        always {
            echo "=== Pipeline Execution Complete ==="
            echo "Duration: ${currentBuild.durationString}"
            sh 'du -sh . || echo "N/A"'
        }
        success {
            echo "[OK] Build SUCCESS for version ${env.BUILD_VERSION}"
            archiveArtifacts artifacts: 'python-app/dist/package/**', fingerprint: true, allowEmptyArchive: true
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
            echo "Workspace cleaned (temporary files removed, package preserved)"
        }
        failure {
            echo "[ERROR] Build FAILED"
            echo "Build Number: ${env.BUILD_NUMBER}"
            archiveArtifacts artifacts: 'python-app/**/*.log, python-app/**/*.pyc', allowEmptyArchive: true
            echo "Workspace preserved for debugging"
        }
        cleanup {
            sh 'rm -rf tmp/ .cache/ .pytest_cache/ || true'
            echo "Cleanup completed"
        }
    }
}
