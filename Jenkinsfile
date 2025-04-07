// Jenkinsfile (Declarative Pipeline)

pipeline {
    // Агент для выполнения пайплайна
    agent {
        // Запускаем сборку внутри Docker-контейнера
        docker {
            image 'eclipse-temurin:21-jdk' // Официальный образ OpenJDK 21 (Temurin)
            // Можно добавить args для монтирования кэша Maven/Gradle для ускорения
            // args '-v $HOME/.m2:/root/.m2' // Пример для Maven. Путь /root/.m2 зависит от пользователя в образе.
            // Убедитесь, что пользователь Jenkins имеет права на $HOME/.m2 на хосте.
        }
    }

    // Инструменты, необходимые для сборки (должны быть настроены в Jenkins)
    tools {
        maven 'Maven3' // Имя вашей конфигурации Maven в Jenkins Global Tool Configuration
    }

    // Переменные окружения для пайплайна
    environment {
        // ID Учетных данных (Credentials ID) для токена SonarQube в Jenkins (тип Secret Text)
        SONAR_CRED_ID = 'SONARQUBE_TOKEN' // <-- ЗАМЕНИТЕ на ваш Credentials ID
        // Имя SonarQube сервера, настроенного в Jenkins -> Configure System -> SonarQube servers
        // Оставьте пустым '', если используется единственный/стандартный сервер.
        SONAR_HOST_NAME = 'MySonarQubeServer' // <-- ЗАМЕНИТЕ на имя вашего сервера SonarQube в Jenkins
        // Уникальный ключ вашего проекта в SonarQube
        // Лучше вынести в параметры Jenkins Job или определить динамически
        SONAR_PROJECT_KEY = 'your-project-key' // <-- ЗАМЕНИТЕ на ключ вашего проекта в SonarQube
    }

    stages {
        stage('Checkout') { // Шаг: Получение исходного кода
            steps {
                // Если используется Multibranch Pipeline или Git SCM в настройках Job,
                // этот шаг обычно выполняется автоматически.
                // Можно добавить явно: checkout scm
                echo "Получение кода..."
                // Для примера, просто выводим сообщение
            }
        }

        stage('Build') { // Шаг: Сборка проекта
            steps {
                // Используем Maven для компиляции, тестов и упаковки
                // 'mvn clean verify' - выполняет тесты и проверки, что важно для SonarQube (покрытие кода)
                // Используйте 'mvn clean package', если тесты запускаются отдельно или не нужны для анализа.
                sh 'mvn clean verify'
            }
        }

        stage('SonarQube Analysis') { // Шаг: Анализ кода с помощью SonarQube
            steps {
                // Используем обертку withSonarQubeEnv для автоматической настройки
                // переменных окружения SONAR_HOST_URL и SONAR_LOGIN (используя SONAR_CRED_ID)
                // 'installationName' должно совпадать с именем сервера в Jenkins Configure System
                withSonarQubeEnv(credentialsId: env.SONAR_CRED_ID, installationName: env.SONAR_HOST_NAME) {
                    // Запускаем анализ SonarQube с помощью Maven плагина
                    // Убедитесь, что sonar-maven-plugin доступен (можно указать в pom.xml или вызвать явно)
                    // Передаем ключ проекта. URL и токен будут установлены `withSonarQubeEnv`.
                    // Можно передать доп. параметры, например, для анализа веток:
                    // -Dsonar.branch.name=${env.BRANCH_NAME} (env.BRANCH_NAME доступна в Multibranch Pipeline)
                    sh "mvn sonar:sonar -Dsonar.projectKey=${env.SONAR_PROJECT_KEY}"
                }
            }
        }

        stage('Quality Gate Status') { // Шаг: Проверка статуса Quality Gate в SonarQube
            steps {
                // Ждем, пока SonarQube обработает отчет анализа (это происходит в фоне)
                // и проверяем статус Quality Gate.
                // timeout: время ожидания (здесь 10 минут).
                // abortPipeline: true - пайплайн упадет, если Quality Gate не пройден (FAILED).
                // SonarQube может вернуть статус WARN, ERROR, OK. Обычно FAILED прерывает сборку.
                waitForQualityGate abortPipeline: true, timeout: 10, unit: 'MINUTES'
            }
        }
    }

    post { // Действия после завершения пайплайна
        always {
            echo 'Пайплайн завершен.'
            // Очистка рабочего пространства (требует плагин Workspace Cleanup)
            // cleanWs()
        }
        success {
            echo 'Сборка и анализ успешно завершены!'
        }
        failure {
            echo 'Сборка или анализ завершились с ошибкой.'
        }
        unstable {
            // Quality Gate может перевести сборку в статус UNSTABLE, а не FAILURE
            echo 'Пайплайн нестабилен (возможно, Quality Gate не пройден).'
        }
    }
}
