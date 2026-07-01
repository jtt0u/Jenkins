def call(Map config = [:]) {
    if (!config.image) {
        error 'Parameter "image" is required'
    }

    def image = config.image
    def tag = config.tag ?: env.BUILD_NUMBER
    def dockerfile = config.dockerfile ?: 'Dockerfile'
    def shouldPush = config.push ?: false
    def registry = config.registry ?: ''
    def fullImageName = registry ? "${registry}/${image}:${tag}" : "${image}:${tag}"

    sh "docker build -f ${dockerfile} -t ${fullImageName} ."

    if (shouldPush) {
        sh "docker push ${fullImageName}"
    }

    return fullImageName
}
