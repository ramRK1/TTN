pipeline{
    
    agent any

    stages{
        stage("Take dump"){
            steps{
                script{
                    def tables = sh(returnStdout: true, script: """
                                mysql -u${env.devmoluser} -p${env.devmolpass} -h"molecule.cvsmskesrzxp.us-east-1.rds.amazonaws.com" --execute="use molecule;show tables;"
                            """).split()
                    def tables_list = String.join(",", tables
                                .stream()
                                .map(name -> ("'" + name + "'"))
                                .collect(Collectors.toList()));
                    echo "$tables_list"
                }
            }
        }
    }
}
