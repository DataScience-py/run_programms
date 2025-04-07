// Jenkinsfile (Declarative Pipeline)

pipeline {
    agent {
        docker {
            // Используем образ, где есть и Maven, и JDK 21
            image 'maven:3.9-eclipse-temurin-21'
            // args '-v $HOME/.m2:/root/.m2' // Можно оставить для кэширования Maven
        }
    }
    // tools { maven 'Maven3' } // Блок tools больше не нужен, т.к. Maven есть в образе
    environment {
        // ... остальные переменные окружения остаются ...
        SONAR_CRED_ID = 'SONARQUBE_TOKEN'
        SONAR_HOST_NAME = 'MySonarQubeServer'
        SONAR_PROJECT_KEY = 'your-project-key'
    }
    stages {
        stage('Checkout') {
            steps {
                echo "Получение кода..."
                checkout scm // Явно добавим checkout, если не используется Multibranch
            }
        }
        stage('Build') {
            steps {
                // Теперь команда mvn должна быть доступна из PATH внутри контейнера
                sh 'mvn clean verify'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv(credentialsId: env.SONAR_CRED_ID, installationName: env.SONAR_HOST_NAME) {
                    // Maven доступен, запускаем анализ
                    sh "mvn sonar:sonar -Dsonar.projectKey=${env.SONAR_PROJECT_KEY}"
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
            // cleanWs() // Очистка рабочего пространства (требует плагин Workspace Cleanup)
        }
        success {
            echo 'Сборка и анализ успешно завершены!'
        }
        failure {
            echo 'Сборка или анализ завершились с ошибкой.'
        }
        unstable {
            // Может быть вызвано Quality Gate (статус WARN) или тестами
            echo 'Пайплайн нестабилен (возможно, Quality Gate не пройден или есть ошибки тестов).'
        }
    }
}
