pipeline {
    agent {
        docker {
            image 'maven:3.9.9-eclipse-temurin-17'
            args '-u root'
        }
    }

    environment {
        DEPLOY_ROOT = 'deployments/test'
        ARTIFACT = 'target/automatizacion-pruebas-1.0.0-SNAPSHOT.jar'
    }

    stages {
        stage('Build') {
            steps {
                sh 'mvn -B -ntp clean package -DskipTests'
            }
        }
        stage('Unit Tests') {
            steps {
                sh 'mvn -B -ntp test'
            }
            post {
                always {
                    junit testResults: 'target/surefire-reports/*.xml', allowEmptyResults: true
                }
            }
        }
        stage('Integration Tests') {
            steps {
                sh 'mvn -B -ntp verify -Pintegration'
            }
            post {
                always {
                    junit testResults: 'target/failsafe-reports/*.xml', allowEmptyResults: true
                }
            }
        }
        stage('Acceptance Gate') {
            steps {
                sh 'mvn -B -ntp verify -Pacceptance'
            }
            post {
                always {
                    junit testResults: 'target/failsafe-reports/*.xml', allowEmptyResults: true
                }
            }
        }
        stage('Deploy to Test - Blue/Green') {
            steps {
                sh 'chmod +x scripts/*.sh'
                sh './scripts/deploy-test.sh "$ARTIFACT"'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'target/*.jar, target/*-reports/**', allowEmptyArchive: true
        }
        failure {
            sh './scripts/rollback.sh || true'
            echo 'Pipeline detenido: se ejecutó el procedimiento de rollback.'
        }
        success {
            echo 'Pipeline completado: build, pruebas y despliegue de prueba exitosos.'
        }
    }
}
