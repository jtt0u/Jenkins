pipeline{
    agent any
    environment {
        DEPLOY_ENV = 'staging'
    }
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

        stage("Deploy to Staging") {
            when {
                environment name: 'DEPLOY_ENV', value: 'staging'
            }
            steps {
                echo "Deploying to staging environment"
                echo "Environment: ${DEPLOY_ENV}"
            }
        }

        stage("Deploy to Production (by env)") {
            when {
                environment name: 'DEPLOY_ENV', value: 'production'
            }
            steps {
                echo "Deploying to production environment"
                echo "Environment: ${DEPLOY_ENV}"
            }
        }
    }
}
