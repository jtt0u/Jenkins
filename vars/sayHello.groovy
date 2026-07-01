def call(Map config = [:]) {
    def name = config.name ?: 'World'
    echo "Hello, ${name}! Build #${env.BUILD_NUMBER}"
}
