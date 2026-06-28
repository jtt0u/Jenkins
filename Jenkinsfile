pipline {
    agent any
    stages {
        stage("List basics") {
            steps{
                script {
                    def envs = ['dev', 'staging', 'production']

                    echo "First: ${envs[0]}"
                    echo "Last: ${envs[-1]}"
                    echo "Each: ${envs.size()}"
                    echo "Added qa: ${envs.add("qa")}"
                    echo "Updated: ${envs}"
                }
            }
        }
    }
}