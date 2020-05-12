pipeline {
   agent any

   stages {
      stage('Build') {
         steps {
            sh "docker build -t 'build' ."
         }
         }
      stage('Run unittest') {
         steps {
            sh "docker run -e SECRET_KEY='This a good aplication' \
                -e MYSQL_HOST='politiccenter.mysql.database.azure.com' \
                -e MYSQL_USER='jlx@politiccenter' \
                -e MYSQL_PASSWORD='politicCenter45' \
                -e MYSQL_DB='politiccenter' \
                build \
                pytest -vv"
         }
         }
      stage('Execute API test') {
         steps {
            sh "docker run -e SECRET_KEY='This a good aplication' \
                -e MYSQL_HOST='politiccenter.mysql.database.azure.com' \
                -e MYSQL_USER='jlx@politiccenter' \
                -e MYSQL_PASSWORD='politicCenter45' \
                -e MYSQL_DB='politiccenter' \
                build \
                ./test/runAllTest.sh"
         }
         }
      stage('Deploy to QA') {
         steps {
            sh "docker stop QA"
            sh "docker rm QA"
            sh "docker run -d -e SECRET_KEY='This a good aplication' \
                -e MYSQL_HOST='politiccenter.mysql.database.azure.com' \
                -e MYSQL_USER='jlx@politiccenter' \
                -e MYSQL_PASSWORD='politicCenter45' \
                -e MYSQL_DB='politiccenter' \
                -p 5000:5000 \
                --name QA \
                build \
                python3 main.py"
         }
         }
      stage('Integration and API test for QA environment') {
         steps {
            sh "docker run -e SECRET_KEY='This a good aplication' \
                -e MYSQL_HOST='politiccenter.mysql.database.azure.com' \
                -e MYSQL_USER='jlx@politiccenter' \
                -e MYSQL_PASSWORD='politicCenter45' \
                -e MYSQL_DB='politiccenter' \
                build \
                ./test/runAllTest.sh"
         }
         }
      stage('Run Performance testing for QA environment') {
         steps {
            sh 'docker run --volume $PWD/test:/mnt/locust -e LOCUSTFILE_PATH=/mnt/locust/locustfile.py -e TARGET_URL=https://shielded-peak-02148.herokuapp.com/ -e LOCUST_OPTS="--clients=2 --no-web --run-time=30" locustio/locust'
         }
         }
      stage('Deploy to Pre-Staging') {
         steps {
            sh "docker stop staging"
            sh "docker rm staging"
            sh "docker run -d -e SECRET_KEY='This a good aplication' \
                -e MYSQL_HOST='politiccenter.mysql.database.azure.com' \
                -e MYSQL_USER='jlx@politiccenter' \
                -e MYSQL_PASSWORD='politicCenter45' \
                -e MYSQL_DB='politiccenter' \
                -p 5001:5000 \
                --name staging \
                build \
                python3 main.py"
         }
         }
      stage('Integration and API test for staging environment') {
         steps {
            sh "docker run -e SECRET_KEY='This a good aplication' \
                -e MYSQL_HOST='politiccenter.mysql.database.azure.com' \
                -e MYSQL_USER='jlx@politiccenter' \
                -e MYSQL_PASSWORD='politicCenter45' \
                -e MYSQL_DB='politiccenter' \
                build \
                ./test/runAllTest.sh"
         }
         }
      }
      stage('Run Performance testing for staging environment') {
         steps {
            sh 'docker run --volume $PWD/test:/mnt/locust -e LOCUSTFILE_PATH=/mnt/locust/locustfile.py -e TARGET_URL=https://shielded-peak-02148.herokuapp.com/ -e LOCUST_OPTS="--clients=2 --no-web --run-time=30" locustio/locust'
         }
         }
   }
