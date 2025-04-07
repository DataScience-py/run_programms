// Jenkinsfile (Declarative Pipeline)

pipeline {
    agent {
        docker {
            // Используем образ, где есть и Maven, и JDK 21
            image 'maven:3.9-eclipse-temurin-21'
            // Если вы хотите кэшировать .m2 репозиторий между сборками на хосте:
            // 1. Убедитесь, что директория /path/to/host/m2repo существует и ДОСТУПНА ДЛЯ ЗАПИСИ пользователю jenkins (UID 122) на ХОСТЕ.
            // 2. Раскомментируйте следующую строку args:
            // args '-v /path/to/host/m2repo:/var/maven/repository:rw,z' // Замените /path/to/host/m2repo на реальный путь
        }
    }
    // tools не нужен, если Maven в образе

    environment {
        SONAR_CRED_ID = 'SONARQUBE_TOKEN' // <-- ЗАМЕНИТЕ на ваш Credentials ID
        SONAR_HOST_NAME = 'MySonarQubeServer' // <-- ЗАМЕНИТЕ на имя вашего сервера SonarQube в Jenkins
        SONAR_PROJECT_KEY = 'your-project-key' // <-- ЗАМЕНИТЕ на ключ вашего проекта в SonarQube

        // Определяем путь для локального репозитория Maven внутри контейнера
        // Вариант 1: Использовать директорию внутри рабочего пространства (не кэшируется между сборками, если workspace очищается)
        MAVEN_REPO_LOCAL = ".m2/repository"
        // Вариант 2: Использовать путь, смонтированный через args -v (если используете кэширование)
        // MAVEN_REPO_LOCAL = "/var/maven/repository" // Должен совпадать с путем в args -v
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Получение кода..."
                checkout scm
            }
        }

        stage('Build') {
            steps {
                // Диагностика (можно будет убрать после успешного запуска)
                sh 'echo "--- DIAGNOSTICS ---"'
                sh 'whoami'
                sh 'id'
                sh 'echo "HOME env var: [$HOME]"' // Посмотрим, установлена ли HOME
                sh 'pwd' // Убедимся, что мы в /var/lib/jenkins/workspace/test
                sh 'echo "--- END DIAGNOSTICS ---"'

                // Запускаем Maven, явно указывая путь к локальному репозиторию
                // Используем переменную MAVEN_REPO_LOCAL из environment
                sh "mvn -Dmaven.repo.local='${env.MAVEN_REPO_LOCAL}' clean verify"
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv(credentialsId: env.SONAR_CRED_ID, installationName: env.SONAR_HOST_NAME) {
                    // Также передаем путь к локальному репозиторию
                    sh "mvn -Dmaven.repo.local='${env.MAVEN_REPO_LOCAL}' sonar:sonar -Dsonar.projectKey=${env.SONAR_PROJECT_KEY}"
                }
            }
        }

        stage('Quality Gate Status') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            echo 'Пайплайн завершен.'
            // cleanWs()
        }
        success {
            echo 'Сборка и анализ успешно завершены!'
        }
        failure {
            echo 'Сборка или анализ завершились с ошибкой.'
        }
        unstable {
            echo 'Пайплайн нестабилен.'
        }
    }
}
