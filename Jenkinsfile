pipeline{
    agent any
    stages {
        stage('Variables Demo') {
            script {
                def appName = 'MyApplication'
                def port = 8080
                def isProduction = false
                echo "App Name is ${appName}"
                echo "Is this production?: ${isProduction}"
                echo "App port: 3000:${port}"
            }
        }

        stage('String Operations') {
            script {
                def message = "Jenkins Pipeline Tutorial"
                echo "Length: ${message.length()}"
                echo "Upper: ${message.toUpperCase()}"
                echo "Lower: ${message.toLowerCase()}"
                def message.replace('Tutorial', 'Course')
                echo "NewEnv: ${message)}"
            }
        }

        stage('Build Version') {
            script {
                def major = '1'
                def minor = '0'
                def patch = "${env.BUILD_NUMBER}"
                env.APP_VERSION = "${major}.${minor}.${patch}"
                echo "Application version: ${env.APP_VERSION}"
            }
        }

        stage('Display Version') {
            script {
                echo "Using version: ${env.APP_VERSION}"
                def imageName = "myapp:${env.APP_VERSION}"
                echo "Docker image would be: ${imageName}"
            }
        }
    }
}