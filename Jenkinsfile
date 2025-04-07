// Jenkinsfile (Declarative Pipeline)

pipeline {
    agent {
        docker {
            image 'eclipse-temurin:21-jdk' // Официальный образ OpenJDK 21 (Temurin)
            // args '-v $HOME/.m2:/root/.m2' // Пример для монтирования кэша Maven. Проверьте путь '/root/.m2' для пользователя в образе.
        }
    }

    tools {
        // !!! ВАЖНО: Убедитесь, что имя 'Maven3' ТОЧНО совпадает
        // с именем Maven, настроенным в Jenkins -> Global Tool Configuration !!!
        maven 'Maven3'
    }

    environment {
        SONAR_CRED_ID = 'SONARQUBE_TOKEN' // <-- ЗАМЕНИТЕ на ваш Credentials ID
        SONAR_HOST_NAME = 'MySonarQubeServer' // <-- ЗАМЕНИТЕ на имя вашего сервера SonarQube в Jenkins
        SONAR_PROJECT_KEY = 'your-project-key' // <-- ЗАМЕНИТЕ на ключ вашего проекта в SonarQube
        // Можно добавить переменную для ветки, если используется Multibranch Pipeline
        // SONAR_BRANCH_NAME = env.BRANCH_NAME ?: 'main' // Использует имя ветки из Jenkins или 'main' по умолчанию
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Получение кода..."
                // Обычно выполняется автоматически (Multibranch) или через SCM в настройках Job
                // checkout scm
            }
        }

        stage('Build') {
            steps {
                // Очистка, компиляция, тесты, упаковка
                sh 'mvn clean verify'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv(credentialsId: env.SONAR_CRED_ID, installationName: env.SONAR_HOST_NAME) {
                    // Запускаем анализ SonarQube с помощью Maven
                    // Добавляем параметры, если нужно (например, для веток)
                    // sh "mvn sonar:sonar -Dsonar.projectKey=${env.SONAR_PROJECT_KEY} -Dsonar.branch.name=${env.SONAR_BRANCH_NAME}"
                    sh "mvn sonar:sonar -Dsonar.projectKey=${env.SONAR_PROJECT_KEY}"
                }
            }
        }

        stage('Quality Gate Status') {
            steps {
                // Оборачиваем waitForQualityGate в блок timeout
                // Указываем время ожидания и единицы измерения для блока timeout
                timeout(time: 10, unit: 'MINUTES') {
                    // Сам waitForQualityGate проверяет статус.
                    // abortPipeline: true - прервет сборку, если статус FAILED.
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
