pipeline{
    agent none

    stage('Check Agent') {
        agent any
        steps{
            echo 'Running on agent...'
            sh 'hostname'
            echo 'Workspace: ${WORKSPACE}'
            echo 'Node name: ${NODE_NAME}'
        }
    }
    stage('Build Info') {
        agent any
        steps{
            echo 'Build information...'
            echo 'Build Number: ${BUILD_NUMBER}'
            echo 'Build ID: ${BUILD_ID}'
            echo 'Build URL: ${BUILD_URL}'
        }
    }
}