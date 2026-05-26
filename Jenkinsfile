pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                python -m venv .venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                call .venv\\Scripts\\activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Selenium Tests') {
    steps {
        bat '''
        echo Current directory is:
        cd

        echo Showing project files:
        dir

        echo Showing tests folder:
        dir tests

        echo Showing pages folder:
        dir pages

        if not exist reports mkdir reports
        if not exist screenshots mkdir screenshots

        call .venv\\Scripts\\activate.bat

        python -m pytest -v --junitxml=reports\\results.xml --html=reports\\report.html --self-contained-html
        '''
    }
}
    }

    post {
        always {
            junit 'reports/results.xml'

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