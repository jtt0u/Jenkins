pipeline{
    agent any
    stages {
        stage("Build") {
            steps {
                echo "Building application..."
                echo "Current branch: ${env.BRANCH_NAME}"
            }
        }

        stage("Deploy to Production") {
            when {
                branch 'main'
            }
            steps {
                echo "Deploying to production environment"
                echo "Branch: main - deployment allowed"
            }
        }
    }
}