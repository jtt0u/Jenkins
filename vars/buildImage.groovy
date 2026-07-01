def call(Map config = [:]) {
    if (!config.image) {
        error 'Parameter "image" is required'
    }

    def image = config.image
    def tag = config.tag ?: env.BUILD_NUMBER
    def dockerfile = config.dockerfile ?: 'Dockerfile'
    def fullImageName = "${image}:${tag}"

    sh "docker build -f ${dockerfile} -t ${fullImageName} ."

    return fullImageName
}
