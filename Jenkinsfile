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
                    sh 'pip3 install -r requirements.txt'
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
    }
}
