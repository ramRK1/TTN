pipeline{
    
    agent any

    stages{
        stage("parameter"){
            steps{
                withCredentials([usernamePassword(credentialsId: 'mol-dev', passwordVariable: 'pass', usernameVariable: 'user')]) {
                    def tables = sh(returnStdout: true, script: """
                                mysql -u$user -p$pass -h"molecule.cvsmskesrzxp.us-east-1.rds.amazonaws.com" --execute="use molecule;show tables;"
                            """).trim()
                    println tables
                }
            }
        }
    }
}