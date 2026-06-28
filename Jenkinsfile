pipeline {
    agent any
    stages {
        stage("List basics") {
            steps {
                script {
                    def envs = ['dev', 'staging', 'production']

                    echo "First: ${envs[0]}"
                    echo "Last: ${envs[-1]}"
                    echo "Each: ${envs.size()}"
                    envs.add("qa")
                    echo "Updated: ${envs}"
                }
            }
        }

        stage("Deploy to Servers") {
            steps {
                script {
                    def servers = ['server1.example.com', 'server2.example.com', 'server3.example.com']

                    for (server in servers) {
                        echo "Deploying to ${server}"
                        sleep 1
                        echo "Deployment to ${server} completed"
                    }
                }
            }
        }

        stage("Configuration Map") {
            steps {
                script {
                    def config = [
                        appName: 'MyWebApp',
                        version: '2.0.0',
                        port: '8080',
                        environment: 'production'
                    ]

                    for (var in config) {
                        echo "${var}"
                    }

                    echo "${config.size()}"
                    config.region = "us-east-1"
                    echo "${config}"
                }
            }
        }

        stage("Environment Variables") {
            steps {
                script {
                    def config = [
                        'DATABASE_URL': 'postgresql://db.example.com:5432/mydb'
                        'CACHE_URL': 'redis://cache.example.com:6379'
                        'LOG_LEVEL': 'info'
                    ]

                    config.each { envName, value ->
                        echo "${envName} = ${value}"
                    }
                }
            }
        }
    }
}