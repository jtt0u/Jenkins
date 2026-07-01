def call(Map config = [:]) {
    if (!config.app) {
        error 'Parameter "app" is required'
    }
    if (!config.version) {
        error 'Parameter "version" is required'
    }

    def environment = config.env ?: 'dev'
    def template = libraryResource('templates/config.properties')
    def content = template
        .replace('{{APP_NAME}}', config.app)
        .replace('{{VERSION}}', config.version)
        .replace('{{ENV}}', environment)

    writeFile file: 'config.properties', text: content
    sh 'cat config.properties'
}
