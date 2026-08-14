pipeline {
    agent any

    environment {
        BACKEND_ACR  = 'backenddivay.azurecr.io'
        FRONTEND_ACR = 'frontenddivay.azurecr.io'

        BACKEND_IMAGE  = "${BACKEND_ACR}/backend"
        FRONTEND_IMAGE = "${FRONTEND_ACR}/frontend"

        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Test') {
            steps {
                sh '''
                    echo "Running backend tests..."
                    # Add your actual test command here
                    # Example:
                    # cd backend
                    # pip install -r requirements.txt
                    # pytest
                '''
            }
        }

        stage('Build Backend Image') {
            steps {
                sh '''
                    docker build \
                      -t ${BACKEND_IMAGE}:${IMAGE_TAG} \
                      -t ${BACKEND_IMAGE}:latest \
                      ./backend
                '''
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh '''
                    docker build \
                      -t ${FRONTEND_IMAGE}:${IMAGE_TAG} \
                      -t ${FRONTEND_IMAGE}:latest \
                      ./frontend
                '''
            }
        }

        stage('Login to Azure') {
            steps {
                sh '''
                    az login --identity
                '''
            }
        }

        stage('Login to Backend ACR') {
            steps {
                sh '''
                    az acr login --name backenddivay
                '''
            }
        }

        stage('Login to Frontend ACR') {
            steps {
                sh '''
                    az acr login --name frontenddivay
                '''
            }
        }

        stage('Push Backend Image') {
            steps {
                sh '''
                    docker push ${BACKEND_IMAGE}:${IMAGE_TAG}
                    docker push ${BACKEND_IMAGE}:latest
                '''
            }
        }

        stage('Push Frontend Image') {
            steps {
                sh '''
                    docker push ${FRONTEND_IMAGE}:${IMAGE_TAG}
                    docker push ${FRONTEND_IMAGE}:latest
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD: Images successfully pushed to ACR.'
        }

        failure {
            echo 'CI/CD: Pipeline failed.'
        }
    }
}