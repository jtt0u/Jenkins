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
                def message.replace('Course')
                echo "NewEnv: ${message)}"
            }
        }
    }
}