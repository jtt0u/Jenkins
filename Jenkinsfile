pipeline{
    agent{
        label any
    }
    stages{
        stage("Build"){
            steps{
                echo "Building application..."
                sh 'mkdir build'
                sh 'echo "Application binary" > build/app.jar'
            }
        }
    }
    post{
        always{
            echo "=== Post Actions ==="
            echo "Pipeline completed"
            sh 'date'
        }
    }
}