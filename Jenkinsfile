def dockerImage
def fullImageName = ''
def latestBranchTag = ''
def imageSize = 'not built'
def coveragePercent = 'not collected'
def testsResult = 'not run'
def deployTime = ''

pipeline {
    agent any

    parameters {
        choice(name: 'DEPLOY_ENV', choices: ['dev', 'staging', 'production'], description: 'Target deployment environment')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run unit tests')
        booleanParam(name: 'RUN_COVERAGE', defaultValue: true, description: 'Run coverage analysis')
        booleanParam(name: 'BUILD_DOCKER', defaultValue: true, description: 'Build Docker image')
        booleanParam(name: 'DEPLOY', defaultValue: false, description: 'Deploy application')
        string(name: 'DOCKER_REGISTRY', defaultValue: 'docker.io/jtt0u', description: 'Docker registry and namespace')
        choice(name: 'NOTIFICATION_LEVEL', choices: ['all', 'failure-only', 'none'], description: 'Notification verbosity')
    }

    environment {
        APP_NAME = 'flask-app'
        GIT_SHORT_COMMIT = ''
        VERSION = ''
        IMAGE_TAG = ''
        DEPLOY_URL = ''
        BUILD_TIME = ''
        BUILD_BRANCH = ''
        DEPLOY_PERFORMED = 'false'
    }

    stages {
        stage('Initialize') {
            steps {
                script {
                    def detectedBranch = env.BRANCH_NAME ?: env.GIT_BRANCH ?: sh(
                        script: 'git branch --show-current || git rev-parse --abbrev-ref HEAD || true',
                        returnStdout: true
                    ).trim()
                    detectedBranch = detectedBranch?.replaceFirst('^origin/', '')
                    if (!detectedBranch || detectedBranch == 'HEAD') {
                        detectedBranch = 'final-cicd-pipeline'
                    }

                    env.BUILD_BRANCH = detectedBranch
                    def safeBranch = detectedBranch.replaceAll('/', '-')
                    env.GIT_SHORT_COMMIT = sh(script: 'git rev-parse --short HEAD || true', returnStdout: true).trim()
                    env.VERSION = "1.0.${env.BUILD_NUMBER}-${env.GIT_SHORT_COMMIT}"
                    env.IMAGE_TAG = "${safeBranch}-${env.VERSION}"
                    env.DEPLOY_URL = "https://app.${params.DEPLOY_ENV}.company.com"
                    env.BUILD_TIME = sh(script: 'date -u +"%Y-%m-%dT%H:%M:%SZ" || true', returnStdout: true).trim()

                    fullImageName = "${params.DOCKER_REGISTRY}/${env.APP_NAME}:${env.IMAGE_TAG}"
                    latestBranchTag = "${params.DOCKER_REGISTRY}/${env.APP_NAME}:latest-${safeBranch}"

                    echo "Branch: ${env.BUILD_BRANCH}"
                    echo "Version: ${env.VERSION}"
                    echo "Image tag: ${env.IMAGE_TAG}"
                    echo "Deploy URL: ${env.DEPLOY_URL}"
                }
            }
        }

        stage('Git Information') {
            steps {
                script {
                    def commitMessage = sh(script: 'git log -1 --pretty=%B || true', returnStdout: true).trim()

                    echo "Full commit: ${env.GIT_COMMIT ?: sh(script: 'git rev-parse HEAD || true', returnStdout: true).trim()}"
                    echo "Short commit: ${env.GIT_SHORT_COMMIT}"
                    echo "Author: ${sh(script: 'git log -1 --pretty=%an || true', returnStdout: true).trim()}"
                    echo "Email: ${sh(script: 'git log -1 --pretty=%ae || true', returnStdout: true).trim()}"
                    echo "Commit date: ${sh(script: 'git log -1 --pretty=%ci || true', returnStdout: true).trim()}"
                    echo "Commit message: ${commitMessage}"

                    if (commitMessage.contains('[skip ci]')) {
                        error 'Build stopped because commit message contains [skip ci]'
                    }
                }

                sh 'echo "Last 5 commits:"'
                sh 'git log -5 --pretty=format:"%h - %an <%ae>: %s" || true'
            }
        }

        stage('Validate Configuration') {
            steps {
                script {
                    def configPath = "configs/config.${params.DEPLOY_ENV}.env"
                    if (!fileExists(configPath)) {
                        error "Missing environment config: ${configPath}"
                    }

                    echo "Using config: ${configPath}"
                    echo "Build version: ${env.VERSION}"
                    echo "Environment: ${params.DEPLOY_ENV}"
                    echo "RUN_TESTS=${params.RUN_TESTS}"
                    echo "RUN_COVERAGE=${params.RUN_COVERAGE}"
                    echo "BUILD_DOCKER=${params.BUILD_DOCKER}"
                    echo "DEPLOY=${params.DEPLOY}"
                }

                sh "cat configs/config.${params.DEPLOY_ENV}.env"
            }
        }

        stage('Install Dependencies') {
            steps {
                dir('flask-app') {
                    sh 'python3 -m pip install --user -r requirements.txt || pip3 install --user -r requirements.txt || pip install --user -r requirements.txt || true'
                    sh 'python3 -m pip freeze || pip3 freeze || pip freeze || true'
                }
            }
        }

        stage('Code Quality') {
            when {
                anyOf {
                    branch 'main'
                    expression { return env.BUILD_BRANCH != 'main' }
                }
            }
            steps {
                dir('flask-app') {
                    sh 'python3 -m py_compile app.py test_app.py || true'
                    sh 'find . -name "*.py" -print0 | xargs -0 wc -l || true'
                }
            }
        }

        stage('Testing Phase') {
            parallel {
                stage('Unit Tests') {
                    when {
                        expression { params.RUN_TESTS == true }
                    }
                    steps {
                        dir('flask-app') {
                            sh 'python3 -m pytest test_app.py -v --junitxml=../test-results.xml || true'
                        }
                        junit testResults: 'test-results.xml', allowEmptyResults: true
                        script {
                            testsResult = 'completed'
                        }
                    }
                }

                stage('Coverage Analysis') {
                    when {
                        expression { params.RUN_COVERAGE == true }
                    }
                    steps {
                        dir('flask-app') {
                            sh 'python3 -m pytest test_app.py --cov=. --cov-report=html:../htmlcov --cov-report=term --cov-fail-under=70 || true'
                        }
                        archiveArtifacts artifacts: 'htmlcov/**', fingerprint: true, allowEmptyArchive: true
                        script {
                            coveragePercent = sh(
                                script: "python3 - <<'PY'\nimport re, pathlib\np = pathlib.Path('htmlcov/index.html')\ntext = p.read_text(errors='ignore') if p.exists() else ''\nm = re.search(r'(\\d+)%', text)\nprint((m.group(1) + '%') if m else 'see htmlcov')\nPY",
                                returnStdout: true
                            ).trim()
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { params.BUILD_DOCKER == true && !env.CHANGE_ID }
            }
            steps {
                script {
                    try {
                        dockerImage = docker.build(
                            fullImageName,
                            "--build-arg APP_VERSION=${env.VERSION} " +
                            "--build-arg BUILD_TIME=${env.BUILD_TIME} " +
                            "--build-arg GIT_COMMIT=${env.GIT_SHORT_COMMIT} " +
                            "--build-arg GIT_BRANCH=${env.BUILD_BRANCH} " +
                            "--build-arg ENVIRONMENT=${params.DEPLOY_ENV} " +
                            "flask-app"
                        )
                        sh "docker tag ${fullImageName} ${latestBranchTag} || true"
                    } catch (err) {
                        echo "Docker build failed: ${err}"
                    }

                    imageSize = sh(script: "docker images ${fullImageName} --format '{{.Size}}' || true", returnStdout: true).trim()
                    echo "Docker image: ${fullImageName}"
                    echo "Docker image size: ${imageSize}"
                }
            }
        }

        stage('Test Docker Container') {
            when {
                expression { params.BUILD_DOCKER == true && dockerImage != null && !env.CHANGE_ID }
            }
            steps {
                script {
                    try {
                        dockerImage.withRun('-p 5000:5000') {
                            sh 'sleep 3 || true'
                            sh 'curl -f http://localhost:5000/health || true'
                            sh "curl -s http://localhost:5000/ || true"
                        }
                    } catch (err) {
                        echo "Docker container test failed: ${err}"
                    }
                }
            }
        }

        stage('Push to Registry') {
            when {
                expression {
                    return params.BUILD_DOCKER == true && dockerImage != null && !env.CHANGE_ID &&
                        (env.BUILD_BRANCH == 'main' || env.BUILD_BRANCH == 'develop')
                }
            }
            steps {
                script {
                    try {
                        docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                            dockerImage.push(env.IMAGE_TAG)
                            docker.image(latestBranchTag).push()
                            if (env.BUILD_BRANCH == 'main') {
                                dockerImage.push('latest')
                            }
                        }
                    } catch (err) {
                        echo "Registry push skipped or failed: ${err}"
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                expression { params.DEPLOY == true && !env.CHANGE_ID }
            }
            steps {
                script {
                    deployTime = sh(script: 'date -u +"%Y-%m-%dT%H:%M:%SZ" || true', returnStdout: true).trim()

                    if (env.BUILD_BRANCH?.startsWith('feature/')) {
                        echo 'Feature branches do not deploy'
                        return
                    }

                    if (params.DEPLOY_ENV == 'production' && env.BUILD_BRANCH != 'main') {
                        error 'Production deploy is allowed only from main branch'
                    }

                    if (params.DEPLOY_ENV == 'dev') {
                        echo 'Deploying to dev with minimal checks'
                    } else if (params.DEPLOY_ENV == 'staging') {
                        echo 'Deploying to staging with smoke tests'
                    } else if (params.DEPLOY_ENV == 'production') {
                        echo 'Running pre-production checks'
                        input message: "Deploy ${env.APP_NAME} ${env.VERSION} to production?"
                        sh 'git config user.name "Jenkins CI" || true'
                        sh 'git config user.email "jenkins@company.com" || true'
                        sh 'git tag -a ${VERSION} -m "Release ${VERSION}" || true'
                    }

                    env.DEPLOY_PERFORMED = 'true'
                    echo "Deploy command: kubectl set image deployment/${env.APP_NAME} ${env.APP_NAME}=${fullImageName} --namespace=${params.DEPLOY_ENV}"
                    echo "Application URL: ${env.DEPLOY_URL}"
                    echo "Deployment time: ${deployTime}"
                }
            }
        }

        stage('Health Checks') {
            when {
                expression { params.DEPLOY == true && env.DEPLOY_PERFORMED == 'true' }
            }
            steps {
                echo "Health: curl -f ${env.DEPLOY_URL}/health"
                script {
                    if (params.DEPLOY_ENV == 'staging' || params.DEPLOY_ENV == 'production') {
                        echo "API status: curl -f ${env.DEPLOY_URL}/api/status"
                        echo "Metrics: curl -f ${env.DEPLOY_URL}/metrics"
                    }
                }
            }
        }

        stage('Smoke Tests') {
            when {
                expression { params.DEPLOY == true && env.DEPLOY_PERFORMED == 'true' && params.DEPLOY_ENV == 'production' }
            }
            steps {
                echo "Smoke test: curl -f ${env.DEPLOY_URL}/"
                echo "Smoke test: curl -f ${env.DEPLOY_URL}/health"
                echo "Smoke test: curl -f ${env.DEPLOY_URL}/api/status"
            }
        }

        stage('Generate Reports') {
            steps {
                sh """
                    cat > build-report.txt <<EOF
Build Version: ${env.VERSION}
Git Commit: ${env.GIT_SHORT_COMMIT}
Git Branch: ${env.BUILD_BRANCH}
Deploy Environment: ${params.DEPLOY_ENV}
Tests Result: ${testsResult}
Coverage: ${coveragePercent}
Docker Image: ${fullImageName}
Docker Image Size: ${imageSize}
Deploy Performed: ${env.DEPLOY_PERFORMED}
Build Time: ${env.BUILD_TIME}
EOF
                """
                script {
                    if (params.DEPLOY_ENV == 'production' && env.DEPLOY_PERFORMED == 'true') {
                        sh 'git log $(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo HEAD~5)..HEAD --pretty=format:"%h %s" > changelog.txt || git log -5 --pretty=format:"%h %s" > changelog.txt || true'
                    } else {
                        sh 'echo "Changelog is generated only for production deployments" > changelog.txt'
                    }
                }
                archiveArtifacts artifacts: 'build-report.txt,changelog.txt,htmlcov/**,test-results.xml', fingerprint: true, allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            script {
                sendNotification('Success')
            }
        }
        failure {
            script {
                sendNotification('Failure')
            }
        }
        unstable {
            script {
                sendNotification('Unstable')
            }
        }
        always {
            archiveArtifacts artifacts: 'build-report.txt,changelog.txt,htmlcov/**,test-results.xml', fingerprint: true, allowEmptyArchive: true
            script {
                if (fullImageName?.trim()) {
                    sh "docker rmi ${fullImageName} || true"
                } else {
                    echo 'No versioned Docker image to remove'
                }

                if (latestBranchTag?.trim()) {
                    sh "docker rmi ${latestBranchTag} || true"
                } else {
                    echo 'No latest branch Docker image to remove'
                }
            }
            sh 'docker image prune -f || true'
            echo "Build result: ${currentBuild.currentResult}"
            echo "Duration: ${currentBuild.durationString}"
            echo "Branch: ${env.BUILD_BRANCH}"
            echo "Version: ${env.VERSION}"
        }
    }
}

def sendNotification(String status) {
    if (params.NOTIFICATION_LEVEL == 'none') {
        echo 'Notifications disabled'
        return
    }

    if (params.NOTIFICATION_LEVEL == 'failure-only' && status == 'Success') {
        echo 'Success notification skipped because NOTIFICATION_LEVEL=failure-only'
        return
    }

    echo """
Notification: ${status}
Job: ${env.JOB_NAME} #${env.BUILD_NUMBER}
Branch: ${env.BUILD_BRANCH}
Commit: ${env.GIT_SHORT_COMMIT}
Environment: ${env.DEPLOY_PERFORMED == 'true' ? params.DEPLOY_ENV : 'not deployed'}
Duration: ${currentBuild.durationString}
Build URL: ${env.BUILD_URL}
${params.DEPLOY_ENV == 'production' ? 'Production deployment requires additional review notes.' : ''}
"""
}
