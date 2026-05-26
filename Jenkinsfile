pipeline {
    agent any

    environment {
        PYTHON_EXE = 'C:\\Users\\Lenovo\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                bat '''
                "%PYTHON_EXE%" --version
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                "%PYTHON_EXE%" -m venv .venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                call .venv\\Scripts\\activate.bat
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat '''
                if exist reports rmdir /s /q reports
                if exist screenshots rmdir /s /q screenshots

                mkdir reports
                mkdir screenshots

                call .venv\\Scripts\\activate.bat

                python -m pytest -v --junitxml=reports\\results.xml --html=reports\\report.html --self-contained-html
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/results.xml'

            publishHTML(target: [
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Selenium HTML Report',
                keepAll: true,
                alwaysLinkToLastBuild: true,
                allowMissing: true
            ])

            archiveArtifacts artifacts: 'screenshots/*.png', allowEmptyArchive: true
            archiveArtifacts artifacts: 'reports/*', allowEmptyArchive: true
        }
    }
}