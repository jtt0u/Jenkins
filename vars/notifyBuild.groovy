def call(Map config = [:]) {
    if (!config.status) {
        error 'Parameter "status" is required'
    }
    if (!config.service) {
        error 'Parameter "service" is required'
    }

    def status = config.status
    def service = config.service
    def channel = config.channel ?: '#builds'

    echo """
Sending notification to ${channel}
Service: ${service}
Status: ${status}
Build: #${env.BUILD_NUMBER}
Build URL: ${env.BUILD_URL}
"""
}
