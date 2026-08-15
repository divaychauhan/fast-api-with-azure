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

        stage('Deploy to App VM') {
            steps {
                sshagent(['app-vm-ssh']) {

                    sh '''
                        set -e

                        echo "Connecting to App VM..."

                        ssh -o StrictHostKeyChecking=no \
                            azureuser@10.0.2.4 << 'EOF'

                        set -e

                        echo "================================"
                        echo " APP VM DEPLOYMENT STARTED"
                        echo "================================"

                        echo "Logging into Azure..."
                        az login --identity

                        echo "Logging into Backend ACR..."
                        az acr login --name backenddivay

                        echo "Logging into Frontend ACR..."
                        az acr login --name frontenddivay

                        echo "Pulling Backend image..."
                        docker pull backenddivay.azurecr.io/backend:latest

                        echo "Pulling Frontend image..."
                        docker pull frontenddivay.azurecr.io/frontend:latest

                        echo "Stopping old Backend container..."
                        docker stop backend || true

                        echo "Removing old Backend container..."
                        docker rm backend || true

                        echo "Stopping old Frontend container..."
                        docker stop frontend || true

                        echo "Removing old Frontend container..."
                        docker rm frontend || true

                        echo "Starting Backend container..."

                        docker run -d \
                            --name backend \
                            --restart unless-stopped \
                            -p 8000:8000 \
                            backenddivay.azurecr.io/backend:latest

                        echo "Starting Frontend container..."

                        docker run -d \
                            --name frontend \
                            --restart unless-stopped \
                            -p 80:80 \
                            frontenddivay.azurecr.io/frontend:latest

                        echo "================================"
                        echo " RUNNING CONTAINERS"
                        echo "================================"

                        docker ps

                        echo "================================"
                        echo " DEPLOYMENT SUCCESSFUL"
                        echo "================================"

                        EOF
                    '''
                }
            }
        }
    }

    post {

        success {
            echo '''
            ============================================
            CI/CD SUCCESS
            Backend and Frontend deployed successfully.
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