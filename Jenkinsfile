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
    }
}