pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "ecommerce"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Evan28-png/e-commerce.git', branch: 'feature/cicd'
            }
        }

        stage('Prepare Environment') {
            steps {
                withCredentials([file(credentialsId: 'db-env-file', variable: 'ENV_FILE')]) {
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
                sh 'pytest test.py'
            }
        }
    }

    post {
        always {
            echo "waiting for 10 mins before cleanup"
            sleep time: 600, unit: 'SECONDS'

            dir('.') {
                sh 'docker-compose down -v'
            }
        }
    }
}