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

        stage("Deploy to Production (by branch)") {
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
                echo "Environment: ${env.DEPLOY_ENV}"
            }
        }

        stage("Deploy to Production") {
            when {
                environment name: 'DEPLOY_ENV', value: 'production'
            }
            steps {
                echo "Deploying to production environment"
                echo "Environment: ${env.DEPLOY_ENV}"
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
                echo "Branch: ${env.BRANCH_NAME}, Environment: ${env.DEPLOY_ENV}"
            }
        }

        stage("Summary") {
            steps {
                echo "=== Pipeline Execution Summary ==="
                echo "Branch: [название ветки]"
                echo "Build Number: [номер]"
                echo "Deploy Environment: [значение DEPLOY_ENV]"
                echo "All stages completed"
            }
        }

        stage('Weekend Task') {
            when {
                expression {
                    def day = new Date().format('EEEE')
                    return day == 'Saturday' || day == 'Sunday'
                }
            }
            steps {
                echo "This is a weekend build!"
                echo "Day: ${new Date().format('EEEE, MMMM dd, yyyy')}"
            }
        }
    }
}
