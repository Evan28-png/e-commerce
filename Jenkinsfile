pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "ecommerce"
        DOCKER_IMAGE="evann23/e-commerce"
        DOCKER_TAG="build-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Evan28-png/e-commerce.git', branch: 'feature/cicd'
            }
        }

        stage('Prepare Environment') {
            steps {
                withCredentials([file(credentialsId: 'env-file', variable: 'ENV_FILE')]) {
                    sh '''
                        echo "Loading env file..."
                        cp $ENV_FILE .env   # Copy into workspace
                    '''
                }
            }
        }
            
        stage('Build & Run') {
            steps {
                dir('.') {
                    sh 'docker-compose build'
                    sh 'docker-compose up -d'
                }
            }    
        }

        stage('Test') {
            steps {
                sh 'docker-compose run --rm app pytest test.py'
            }
        }

        stage('Scan with trivy') {
            steps {
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --timeout 20m --scanners vuln --exit-code 0 --severity HIGH,CRITICAL $DOCKER_IMAGE:$DOCKER_TAG'
            }
        }
        
        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-secret', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $DOCKER_IMAGE:$DOCKER_TAG
                    '''
                }
            }
        }
    }
        

    post {
        always {
            echo "waiting for 6 mins before cleanup"
            sleep time: 360, unit: 'SECONDS'

            dir('.') {
                sh 'docker-compose down -v'
            }
        }
    }
}
