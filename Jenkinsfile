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
        stage('Provision EC2 and Deploy Containers') {
            steps {
            dir('terraform') { // adjust if main.tf is in a different folder
                sh '''
                    # Initialize and apply Terraform
                    terraform init -input=false
                    terraform apply -auto-approve -input=false

                    # Get the public IP of the new EC2 instance
                    PUBLIC_IP=$(terraform output -raw public_ip)
                    echo "EC2 instance public IP: $PUBLIC_IP"

                    # Wait for SSH to become available
                    echo "Waiting for EC2 to be ready for SSH..."
                    for i in {1..20}; do
                    if nc -zv $PUBLIC_IP 22 >/dev/null 2>&1; then
                        echo "SSH is up!"
                        break
                    fi
                    echo "Retrying in 15s..."
                    sleep 15
                    done

                    # SSH into the instance and run Docker commands
                    ssh -o StrictHostKeyChecking=no -i ~/.ssh/your_key.pem ec2-user@$PUBLIC_IP << 'EOF'
                        sudo apt update -y
                        sudo apt install -y docker
                        sudo systemctl start docker
                        sudo systemctl enable docker

                        # Pull and run your Docker container(s)
                        docker pull $DOCKER_IMAGE:$DOCKER_TAG
                        docker run -d -p 5000:3000 $DOCKER_IMAGE:$DOCKER_TAG 
                    EOF
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
