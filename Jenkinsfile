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

                    if [ -f "backend/Dockerfile" ]; then
                        CONTEXT="backend"

                    elif [ -f "Dockerfile" ]; then
                        CONTEXT="."

                    else
                        echo "ERROR: Backend Dockerfile not found."
                        echo "Repository structure:"
                        find . -maxdepth 3 -type f | sort
                        exit 1
                    fi

                    echo "Backend build context: $CONTEXT"

                    docker build \
                      -t ${BACKEND_ACR}/${BACKEND_REPO}:${IMAGE_TAG} \
                      -t ${BACKEND_ACR}/${BACKEND_REPO}:latest \
                      "$CONTEXT"
                '''
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh '''
                    set -e

                    if [ -f "frontend/Dockerfile" ]; then
                        CONTEXT="frontend"

                    else
                        echo "ERROR: Frontend Dockerfile not found."
                        echo "Repository structure:"
                        find . -maxdepth 3 -type f | sort
                        exit 1
                    fi

                    echo "Frontend build context: $CONTEXT"

                    docker build \
                      -t ${FRONTEND_ACR}/${FRONTEND_REPO}:${IMAGE_TAG} \
                      -t ${FRONTEND_ACR}/${FRONTEND_REPO}:latest \
                      "$CONTEXT"
                '''
            }
        }

        stage('Azure Login') {
            steps {
                sh '''
                    set -e

                    echo "Logging into Azure using Managed Identity..."

                    az login --identity

                    az account show \
                      --query "{subscription:id,tenant:tenantId}" \
                      -o table
                '''
            }
        }

        stage('Login to Backend ACR') {
            steps {
                sh '''
                    set -e

                    echo "Logging into Backend ACR..."

                    az acr login \
                      --name backenddivay
                '''
            }
        }

        stage('Login to Frontend ACR') {
            steps {
                sh '''
                    set -e

                    FRONTEND_ACR_NAME="${FRONTEND_ACR%%.azurecr.io}"

                    if [ "$FRONTEND_ACR_NAME" = "frontenddivay" ]; then
                        echo "ERROR: Set your actual frontend ACR name."
                        exit 1
                    fi

                    echo "Logging into Frontend ACR..."

                    az acr login \
                      --name "$FRONTEND_ACR_NAME"
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