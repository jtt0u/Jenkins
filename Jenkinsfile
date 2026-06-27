pipeline{
    agent any
    stages {
        stage('Variables Demo') {
            steps {
                script {
                    def appName = 'MyApplication'
                    def port = 8080
                    def isProduction = false
                    echo "App Name is ${appName}"
                    echo "Is this production?: ${isProduction}"
                    echo "App port: 3000:${port}"
                }
            }
        }

        stage('String Operations') {
            steps {
                script {
                    def message = "Jenkins Pipeline Tutorial"
                    echo "Length: ${message.length()}"
                    echo "Upper: ${message.toUpperCase()}"
                    echo "Lower: ${message.toLowerCase()}"
                    def newMessage = message.replace('Tutorial', 'Course')
                    echo "NewEnv: ${newMessage}"
                }
            }
        }

        stage('Build Version') {
            steps {
                script {
                    def major = '1'
                    def minor = '0'
                    def patch = "${env.BUILD_NUMBER}"
                    env.APP_VERSION = "${major}.${minor}.${patch}"
                    echo "Application version: ${env.APP_VERSION}"
                }
            }
        }

        stage('Display Version') {
            steps {
                script {
                    echo "Using version: ${env.APP_VERSION}"
                    def imageName = "myapp:${env.APP_VERSION}"
                    echo "Docker image would be: ${imageName}"
                }
            }
        }

        stage('Jenkins Info') {
            steps {
                script {
                    echo "Build number is: ${env.BUILD_NUMBER}"
                    echo "$Build ID is: {env.BUILD_ID}"
                    echo "$Job Name is: {env.JOB_NAME}"
                    echo "$We are in Workspace: {env.WORKSPACE}"
                    echo "$Build URL: {env.BUILD_URL}"
                }
            }
        }
    }
}
