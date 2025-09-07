pipeline {
    agent any

    environment {
       COMPOSE_PROJECT_NAME = "ecommerce"
       JOB_NAME="${env.JOB_NAME}"
    }

    stages {
        stage('Checkout') {
            steps {
                // Clone your GitHub repo (change URL to your repo)
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

        stage('Build & Run') {
            steps {
                // Run docker-compose commands in the repo root so init.sql is accessible
                dir('.') {
		    sh 'export JOB_NAME=$JOB_NAME'
                    sh 'docker-compose build'
                    sh 'docker-compose up -d'
                }
            }
        }

        stage('Test') {
            steps {
		pytest test.py
            }
        }
    }

    post {
        always {
            // Cleanup containers, volumes, networks to avoid leftovers
	    echo "waiting for 10 mins before cleanup"
	    sleep time: 600, unit: 'SECONDS'
	
            dir('.') {
                sh 'docker-compose down -v'
            }
        }
    }
}

