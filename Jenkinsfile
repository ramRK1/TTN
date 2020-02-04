pipeline{
    
    agent any

    stages{
        stage("parameter"){
            steps{
                withCredentials([usernamePassword(credentialsId: 'mol-dev', passwordVariable: 'pass', usernameVariable: 'user')]) {
                    sh """
                        mysql -u$user -p$pass -h"molecule.cvsmskesrzxp.us-east-1.rds.amazonaws.com" --execute="use molecule;show tables;"
                        
                    """
                }
            }
        }
    }
}