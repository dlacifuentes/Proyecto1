pipeline {
    agent any

    environment {
        GIT_REPO_URL   = "https://github.com/dlacifuentes/Proyecto1.git"
        DOCKER_IMAGE   = "dlacifuentes/demo-python-app"
        BUILD_TAG      = "${env.BUILD_NUMBER}"
        CONTAINER_NAME = "api-pedidos"
    }

    parameters {
        booleanParam(
            name: 'DESPLIEGUE',
            defaultValue: false,
            description: 'Si está marcado, ejecuta también CD. Si no, solo CI'
        )
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo "Clonando el repositorio de GitHub..."
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: "${GIT_REPO_URL}" ]])
                echo "Clonación finalizada"
            }
        }

        stage('Instalación de dependencias') {
            steps {
                echo "Instalando dependencias..."
                bat '''
                    python --version
                    pip install --no-cache-dir -r requirements.txt
                '''
                echo "Instalación de dependencias finalizada"
            }
        }

        stage('Ejecución Pruebas Unitarias') {
            steps {
                echo "Ejecutando las pruebas unitarias..."
                bat 'pytest -v'
                echo "Pruebas unitarias finalizadas con éxito"
            }
        }

        stage('Construcción Imagen Docker') {
            when {
                expression { return params.DESPLIEGUE }
            }
            steps {
                echo "Construyendo la imagen de la aplicación..."
                bat "docker build -t %DOCKER_IMAGE%:%BUILD_TAG% ."
                echo "Imagen de Docker creada"
            }
        }

        stage('Publicar Imagen Docker') {
            when {
                expression { return params.DESPLIEGUE }
            }
            steps {
                echo "Publicando la imagen en Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'docker_hub_token', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    bat """
                        echo Iniciando login en Docker Hub... 
                        docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                        docker push %DOCKER_IMAGE%:%BUILD_TAG%
                    """
                }
                echo "Imagen publicada correctamente"
            }
        }

        stage('Despliegue') {
            when {
                expression { return params.DESPLIEGUE }
            }
            steps {
                echo "Desplegando la aplicación..."
                bat '''
                    docker stop %CONTAINER_NAME% 2>null || echo No habia contenedor corriendo
                    docker rm %CONTAINER_NAME% 2>null || echo No habia contenedor para borrar
                    docker run -d --name %CONTAINER_NAME% -p 5000:5000 %DOCKER_IMAGE%:%BUILD_TAG%
                '''
                echo "La API FastAPI debería estar disponible en http://localhost:5000"
            }
        }
    }

    post {
        success {
            echo 'Pipeline ejecutado con éxito'
            emailext (
                subject: "Build OK: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Build ejecutado con éxito</h2>
                    <p>El job <b>${env.JOB_NAME}</b> completó exitosamente.</p>
                    <p>Build #: ${env.BUILD_NUMBER}</p>
                    <p>Ver consola: ${env.BUILD_URL}console</p>
                """,
                to: "dla.cifuentes98@gmail.com",
                mimeType: 'text/html'
            )
        }
        failure {
            echo 'Error en la ejecución del pipeline'
            emailext (
                subject: "Build FALLÓ: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2 style="color:red;">Build Fallida</h2>
                    <p>Revisar detalles en Jenkins:</p>
                    <p><a href="${env.BUILD_URL}console">${env.BUILD_URL}console</a></p>
                """,
                to: "dla.cifuentes98@gmail.com",
                 mimeType: 'text/html'
            )
        }
    }
}
