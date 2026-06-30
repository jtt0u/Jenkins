pipeline {
    agent any

    tools {
        nodejs 'NodeJS 20'
    }

    parameters {
        string(
            name: 'APP_VERSION',
            defaultValue: '1.0.0',
            description: 'Application version to build'
        )
    }

    environment {
        APP_NAME = 'jenkins-sample-app'
        NODE_ENV = 'production'
    }

    stages {
        stage("Build") {
            steps {
                echo "Building ${env.APP_NAME} version ${params.APP_VERSION}"
                dir('app') {
                    sh 'npm install'
                    sh "APP_VERSION=${params.APP_VERSION} npm run build"
                }
                echo "Build completed for version ${params.APP_VERSION}"
            }
        }
    }
}
