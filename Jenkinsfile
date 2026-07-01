pipeline {
    agent any

    environment {
        GIT_SHORT_COMMIT = "${sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()}"
        BUILD_VERSION = "${sh(script: 'printf \"1.0.%s-%s\" \"$BUILD_NUMBER\" \"$(git rev-parse --short HEAD)\"', returnStdout: true).trim()}"
    }

    stages {
        stage('Git Info') {
            steps {
                script {
                    def gitBranch = env.GIT_BRANCH ?: sh(script: 'git branch --show-current', returnStdout: true).trim()
                    def gitCommit = env.GIT_COMMIT ?: sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    def authorName = sh(script: 'git log -1 --pretty=%an', returnStdout: true).trim()
                    def authorEmail = sh(script: 'git log -1 --pretty=%ae', returnStdout: true).trim()
                    def repoUrl = env.GIT_URL ?: sh(script: 'git config --get remote.origin.url', returnStdout: true).trim()

                    echo "Current branch: ${gitBranch}"
                    echo "Full commit hash: ${gitCommit}"
                    echo "Short commit hash: ${env.GIT_SHORT_COMMIT}"
                    echo "Commit author name: ${authorName}"
                    echo "Commit author email: ${authorEmail}"
                    echo "Repository URL: ${repoUrl}"
                    echo "Build version: ${env.BUILD_VERSION}"
                }
            }
        }

        stage('Commit Message') {
            steps {
                script {
                    def commitMessage = sh(
                        script: 'git log -1 --pretty=%B',
                        returnStdout: true
                    ).trim()

                    echo "Last commit message:"
                    echo commitMessage

                    if (commitMessage.contains('[skip ci]')) {
                        echo 'WARNING: Commit message contains [skip ci]'
                    }
                }
            }
        }

        stage('Build') {
            steps {
                dir('flask-app') {
                    sh 'pip install -r requirements.txt || pip3 install -r requirements.txt || python3 -m pip install -r requirements.txt || true'
                    echo "Building version ${env.BUILD_VERSION}"
                }
            }
        }

        stage('Create Git Tag') {
            when {
                branch 'main'
            }
            steps {
                sh 'git config user.name "Jenkins CI"'
                sh 'git config user.email "jenkins@company.com"'
                sh 'git tag -a ${BUILD_VERSION} -m "Build ${BUILD_VERSION}" || true'
                echo "Created local Git tag: ${env.BUILD_VERSION}"
            }
        }

        stage('Git Stats') {
            steps {
                sh 'echo "Commit count:"'
                sh 'git rev-list --count HEAD'

                sh 'echo "Last 5 commits:"'
                sh 'git log -5 --pretty=format:"%h - %an: %s"'

                sh 'echo "Changed files in last commit:"'
                sh 'git diff-tree --no-commit-id --name-only -r HEAD'
            }
        }

        stage('Generate Changelog') {
            steps {
                script {
                    def previousTag = sh(
                        script: 'git describe --tags --abbrev=0 @^ 2>/dev/null || true',
                        returnStdout: true
                    ).trim()

                    if (previousTag) {
                        sh "git log ${previousTag}..@ --pretty=format:'%h %s' > changelog.txt"
                    } else {
                        sh "git log -10 --pretty=format:'%h %s' > changelog.txt"
                    }
                }
                archiveArtifacts artifacts: 'changelog.txt', fingerprint: true, allowEmptyArchive: true
            }
        }
    }
}
