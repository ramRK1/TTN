pipeline{
    
    agent any

    stages{
        stage("Take dump"){
            steps{
                script{
                    withCredentials([usernamePassword(credentialsId: 'mol-dev', passwordVariable: 'pass', usernameVariable: 'user')]) {
                        def tables = sh(returnStdout: true, script: """
                                    mysql -u${env.devmoluser} -p${env.devmolpass} -h"molecule.cvsmskesrzxp.us-east-1.rds.amazonaws.com" --execute="use molecule;show tables;"
                                """).split()
                        echo "$tables"
                    }
                }
            }
        }
    }
}
