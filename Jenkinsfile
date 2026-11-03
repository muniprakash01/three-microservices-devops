pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {

        stage('Git Checkout') {
            steps {
                echo 'Checking out source code'
                checkout scm
            }
        }

        stage('Validate Docker Compose') {
            steps {
                sh 'docker compose -f ${COMPOSE_FILE} config -q'
            }
        }

        stage('Test User Service') {
            steps {
                dir('user-service') {
                    sh '''
                        python3 -m venv .venv
                        .venv/bin/pip install -r requirements.txt
                        .venv/bin/pytest tests/ -v
                    '''
                }
            }
        }

        stage('Test Product Service') {
            steps {
                dir('product-service') {
                    sh '''
                        python3 -m venv .venv
                        .venv/bin/pip install -r requirements.txt
                        .venv/bin/pytest tests/ -v
                    '''
                }
            }
        }

        stage('Test Order Service') {
            steps {
                dir('order-service') {
                    sh '''
                        python3 -m venv .venv
                        .venv/bin/pip install -r requirements.txt
                        .venv/bin/pytest tests/ -v
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                    trivy image --severity HIGH,CRITICAL --exit-code 1 three-microservices-user:latest
                    trivy image --severity HIGH,CRITICAL --exit-code 1 three-microservices-product:latest
                    trivy image --severity HIGH,CRITICAL --exit-code 1 three-microservices-order:latest
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh 'docker compose up -d'
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 15
                    docker compose ps
                    curl --fail http://localhost:5001/health
                    curl --fail http://localhost:5002/health
                    curl --fail http://localhost:5003/health
                '''
            }
        }
    }

    post {
        success {
            echo 'All services deployed successfully'
        }

        failure {
            echo 'Pipeline failed. Check the console output.'
        }

        always {
            sh 'docker compose ps || true'
        }
    }
}
