def call(Map config = [:]) {
    if (!config.app) {
        error 'Parameter "app" is required'
    }
    if (!config.image) {
        error 'Parameter "image" is required'
    }

    def app = config.app
    def image = config.image
    def environment = config.env ?: 'staging'
    def replicas = config.replicas ?: 1
    def manifestFile = "deployment-${environment}.yaml"
    def template = libraryResource('templates/deployment.yaml')
    def manifest = template
        .replace('{{APP_NAME}}', app)
        .replace('{{IMAGE}}', image)
        .replace('{{REPLICAS}}', replicas.toString())
        .replace('{{ENVIRONMENT}}', environment)

    writeFile file: manifestFile, text: manifest

    echo "Deploying ${app} to ${environment}"
    echo "Image: ${image}"
    echo "Replicas: ${replicas}"
    sh "cat ${manifestFile}"
    sh "echo 'kubectl apply -f ${manifestFile}'"
}
