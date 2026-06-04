pipeline {
    agent any

    environment {
        IMAGE_NAME = 'jenkins-ci-demo'
        CONTAINER_NAME = 'jenkins-ci-demo-app'
        APP_PORT = '5000'
    }

    stages {
        stage('Clone') {
            steps {
                echo "Clonage depuis ${env.GIT_URL}"
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Scan Trivy') {
            steps {
                sh '''
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy:latest image \
                        --exit-code 0 \
                        --severity HIGH,CRITICAL \
                        --no-progress \
                        ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Test') {
            steps {
                sh 'docker run --rm ${IMAGE_NAME}:latest python -c "import flask; import prometheus_client; print(\'deps OK\')"'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        --restart unless-stopped \
                        -p ${APP_PORT}:5000 \
                        ${IMAGE_NAME}:latest
                '''
            }
        }
    }

    post {
        success { echo 'Deploy OK ✅' }
        failure { echo 'Pipeline KO ❌' }
    }
}