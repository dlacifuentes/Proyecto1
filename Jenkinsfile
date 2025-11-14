pipeline {
    agent any

    environment {
        GIT_REPO_URL   = "https://github.com/dlacifuentes/Proyecto1.git"
        DOCKER_IMAGE   = "dlacifuentes/demo-python-app"
        BUILD_TAG      = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
        CONTAINER_NAME = "api-pedidos"
        HOST           = "localhost"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Clonando el repositorio de GitHub..."
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: $GIT_REPO_URL ]])
                echo "Clonación finalizada"
            }
        }

        stage('Instalación de dependencias') {
            steps {
                echo "Instalando dependencias..."
                sh 'python --version'
                sh 'pip install --no-cache-dir -r requirements.txt'
                echo "Instalación de dependencias finalizada"
            }
        }

        stage('Ejecución Pruebas Unitarias') {
            steps {
                echo "Ejecutando las pruebas unitarias..."
                sh 'pytest -v'
                echo "Pruebas unitarias finalizadas con éxito"
            }
        }

        stage('Construcción Imagen Docker') {
            steps {
                echo "Construyendo la imagen de la aplicación..."
                IMAGE_TAG = "${BUILD_NUMBER}"

                sh 'docker build -t $DOCKER_IMAGE:${IMAGE_TAG} .'
                ech "Imagen de Docker creada"
            }
        }

        stage('Publicar Imagen Docker') {
            steps {
                echo "Publicando la imagen en Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'docker_hub_token', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $DOCKER_IMAGE:${IMAGE_TAG}'
                }
                echo "Imagen publicada correctamente"
            }
        }

        stage('Despliegue') {
            steps {
                echo "Desplegando la aplicación..."
                sh 'docker run -d --name $CONTAINER_NAME -p 5000:5000 $DOCKER_IMAGE:${IMAGE_TAG}'
                echo "La API FastAPI debería estar disponible en http://$HOST:5000"
            }
        }
    }

    post {
        success {
            echo 'Pipeline ejecutado con éxito'
            /*mail to: 'devteam@empresa.com',
                 subject: "CI/CD pipeline ejecutado con exitoso: ${env.JOB_NAME}",
                 body: "El pipeline ${env.BUILD_NUMBER} finalizó correctamente." */
        }
        failure {
            echo 'Error en la ejecución del pipeline'
        }
    }
}
