pipeline {
    agent any

    tools {
        nodejs 'NodeJS 20'
    }

    environment {
        APP_NAME = 'jenkins-sample-app'
        NODE_ENV = 'production'
        APP_VERSION = "1.0.${BUILD_NUMBER}"
    }

    stages {
        stage("Build") {
            steps {
                dir('app') {
                    sh 'npm install'
                    sh 'npm run build'
                    sh 'echo "Build completed for version $APP_VERSION"'
                }
            }
        }

        stage("Test with API Key") {
            steps {
                withCredentials([
                    string(credentialsId: 'api-key', variable: 'API_KEY')
                ]) {
                    dir('app') {
                        sh 'API_KEY=$API_KEY NODE_ENV=test APP_VERSION=$APP_VERSION npm test'
                        sh 'echo "API key: $API_KEY"'
                        echo "Tests completed with API key configured"
                    }
                }
            }
        }
    }
}
