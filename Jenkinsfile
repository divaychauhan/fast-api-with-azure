pipeline {
    agent any

    environment {
        BACKEND_ACR  = 'backenddivay.azurecr.io'
        FRONTEND_ACR = 'frontenddivay.azurecr.io'

        BACKEND_REPO  = 'backend'
        FRONTEND_REPO = 'frontend'

        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Build Backend Image') {
            steps {
                sh '''
                    set -e

                    echo "Building FastAPI Backend..."

                    docker build \
                      -t ${BACKEND_ACR}/${BACKEND_REPO}:${IMAGE_TAG} \
                      -t ${BACKEND_ACR}/${BACKEND_REPO}:latest \
                      ./fastapi_mognodb
                '''
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh '''
                    set -e

                    echo "Building Frontend..."

                    docker build \
                      -t ${FRONTEND_ACR}/${FRONTEND_REPO}:${IMAGE_TAG} \
                      -t ${FRONTEND_ACR}/${FRONTEND_REPO}:latest \
                      ./aman-tour-travels
                '''
            }
        }

        stage('Azure Login') {
            steps {
                sh '''
                    set -e

                    echo "Logging into Azure using Managed Identity..."

                    az login --identity
                '''
            }
        }

        stage('Login to Backend ACR') {
            steps {
                sh '''
                    set -e

                    echo "Logging into Backend ACR..."

                    az acr login --name backenddivay
                '''
            }
        }

        stage('Login to Frontend ACR') {
            steps {
                sh '''
                    set -e

                    FRONTEND_ACR_NAME="${FRONTEND_ACR%%.azurecr.io}"

                    echo "Logging into Frontend ACR..."

                    az acr login --name "$FRONTEND_ACR_NAME"
                '''
            }
        }

        stage('Push Backend Image') {
            steps {
                sh '''
                    set -e

                    echo "Pushing Backend image..."

                    docker push \
                      ${BACKEND_ACR}/${BACKEND_REPO}:${IMAGE_TAG}

                    docker push \
                      ${BACKEND_ACR}/${BACKEND_REPO}:latest
                '''
            }
        }

        stage('Push Frontend Image') {
            steps {
                sh '''
                    set -e

                    echo "Pushing Frontend image..."

                    docker push \
                      ${FRONTEND_ACR}/${FRONTEND_REPO}:${IMAGE_TAG}

                    docker push \
                      ${FRONTEND_ACR}/${FRONTEND_REPO}:latest
                '''
            }
        }
    }

    post {
        success {
            echo '''
            ============================================
            CI/CD SUCCESS
            Backend and Frontend images pushed to ACR.
            ============================================
            '''
        }

        failure {
            echo '''
            ============================================
            CI/CD FAILED
            Check the failed stage above.
            ============================================
            '''
        }

        always {
            sh 'docker image prune -f || true'
        }
    }
}