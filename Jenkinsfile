pipeline {
   agent any

    environment {
        SECRET_KEY='This a good aplication'
        MYSQL_HOST='politiccenter.c8ks72g1m2ln.us-east-1.rds.amazonaws.com'
        MYSQL_USER='admin'
        MYSQL_PASSWORD='politicCenter45'
        MYSQL_DB='politiccenter'
    }

   stages {
      stage('Clone repo') {
         steps {
            git 'https://github.com/Jlopezjlx/politiccenter_backend.git'
         }
         }
      stage('Build for test') {
         steps {
            sh "docker build -t 'build' ."
         }
         }
      stage('Run unittest') {
         steps {
            sh "docker run build ./test/runAllTest.sh"
         }
         }
      stage('Execute API test') {
         steps {
            sh "docker run build ./test/runAllTest.sh"
         }
         }
      stage('Deploy to QA') {
         steps {
            sh "docker stop QA"
            sh "docker run -d --name QA -p 5000:5000 build python3 main.py"
         }
         }
      stage('Deploy to Pre-Staging') {
         steps {
            sh "docker stop staging"
            sh "docker run -d --name staging -p 5001:5000 build python3 main.py"
         }
         }
      }
   }
