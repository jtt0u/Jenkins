pipeline {
    agent any

    stages {
        stage("Inspect Workspace") {
            steps {
                sh 'pwd'
                sh 'ls -la'
                sh 'du -sh .'
                sh 'echo "Workspace: $WORKSPACE"'
            }
        }

        stage("Create Test Files") {
            steps {
                sh 'echo "test" > test1.txt'
                sh 'mkdir -p temp && echo "temp" > temp/temp.log'
                sh 'mkdir -p old-build && echo "old" > old-build/app.jar'
                sh 'ls -la'
                sh 'find temp old-build -type f -print'
            }
        }
    }
}
