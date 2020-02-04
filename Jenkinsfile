pipeline {
    
    agent any
    
    stages{
        stage("git pull"){
            
        }
        stage("run shell file"){
            steps{
                withCredentials([usernamePassword(credentialsId: 'mol-dev', passwordVariable: 'pass', usernameVariable: 'user')]) {
                    sh """
                        export USER=$user ; export PASSWORD=$pass ; export HOST="molecule.cvsmskesrzxp.us-east-1.rds.amazonaws.com" ; export DATABASE="molecule" ; mysqldump -u$user -p$pass -h"molecule.cvsmskesrzxp.us-east-1.rds.amazonaws.com" --databases molecule > molecule-backup-${BUILD_NUMBER}.sql ; /bin/bash $WORKSPACE/src/db-scripts/db-scripts.sh
                        aws s3 cp molecule-backup-${BUILD_NUMBER}.sql s3://
                    """
                }    
            }
        }
    }
}