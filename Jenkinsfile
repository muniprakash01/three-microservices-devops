
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        COMPOSE_PROJECT_NAME = 'three-microservices'
    }

    stages {

        stage('Git Checkout') {
            steps {
                echo 'Checking out source code from GitHub'
                checkout scm
            }
        }

        stage('Environment Check') {
            steps {
                sh '''
                    echo "Checking Docker installation..."
                    docker --version

                    echo "Checking Docker Compose..."
                    docker compose version

                    echo "Checking Trivy installation..."
                    trivy --version
                '''
            }
        }

        stage('Validate Configuration') {
            steps {
                sh '''
                    echo "Checking project files..."

                    test -f docker-compose.yml
                    test -f user-service/Dockerfile
                    test -f product-service/Dockerfile
                    test -f order-service/Dockerfile

                    echo "Validating Docker Compose configuration..."
                    docker compose config -q
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    echo "Building all microservice images..."
                    docker compose build --pull
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                    echo "Scanning Docker images..."

                    IMAGES=$(docker compose config --images | sort -u)

                    if [ -z "$IMAGES" ]; then
                        echo "ERROR: No image names found."
                        echo "Define an image property for each service in docker-compose.yml."
                        exit 1
                    fi

                    for IMAGE in $IMAGES
                    do
                        echo "Scanning image: $IMAGE"

                        trivy image \
                            --severity HIGH,CRITICAL \
                            --exit-code 1 \
                            "$IMAGE"
                    done
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                    echo "Deploying microservices..."

                    docker compose up -d --remove-orphans
                '''
            }
        }

        stage('Deployment Verification') {
            steps {
                sh '''
                    echo "Checking deployed containers..."

                    docker compose ps

                    for SERVICE in user-service product-service order-service nginx
                    do
                        if ! docker compose ps --status running --services | grep -qx "$SERVICE"; then
                            echo "ERROR: $SERVICE is not running."
                            exit 1
                        fi
                    done

                    echo "All expected services are running."
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Three-Microservices CI/CD Pipeline completed.'
        }

        failure {
            echo 'FAILED: Pipeline encountered an error.'

            sh 'docker compose logs --tail=50 || true'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}
