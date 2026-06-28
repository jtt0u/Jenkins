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

        stage("Deploy to Production") {
            when {
                environment name: 'DEPLOY_ENV', value: 'production'
            }
            steps {
                echo "Deploying to production environment"
                echo "Environment: ${DEPLOY_ENV}"
            }
        }
        
        stage("Run Tests") {
            when {
                expression {
                    return env.BUILD_NUMBER.toInteger() % 2 == 0
                }
            }
            steps {
                echo "Running tests for build ${env.BUILD_NUMBER}"
                echo "This is an even-numbered build"
            }
        }

        stage("Skip Tests") {
            when {
                expression {
                    return env.BUILD_NUMBER.toInteger() % 2 != 0
                }
            }
            steps {
                echo "Skipping tests for build ${env.BUILD_NUMBER}"
                echo "This is an odd-numbered build"
            }
        }

        stage("Security Scan") {
            when {
                allOf {
                    anyOf {
                        branch 'main'
                        branch 'develop'
                    }
                    anyOf {
                        environment name: 'DEPLOY_ENV', value: 'staging'
                        environment name: 'DEPLOY_ENV', value: 'production'
                    }
                }
            }
            steps {
                echo "Running security scan"
                echo "Branch: ${env.BRANCH_NAME}, Environment: ${DEPLOY_ENV}"
            }
        }

        stage("Summery") {
            steps {
                echo "=== Pipeline Execution Summary ==="
                echo "Branch: [название ветки]"
                echo "Build Number: [номер]"
                echo "Deploy Environment: [значение DEPLOY_ENV]"
                echo "All stages completed"
            }
        }
    }
}
