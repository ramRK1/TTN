pipeline{
    
    agent any

    stages{
        stage("Take dump"){
            steps{
                script{
                    def tables = sh(returnStdout: true, script: """
                                mysql -u${env.devmoluser} -p${env.devmolpass} -h"molecule.cvsmskesrzxp.us-east-1.rds.amazonaws.com" --execute="use molecule;show tables;"
                            """).split("\n")
                    echo "$tables"
                    def tables_list = []
                    for (table in tables){
                        def tab = "'"+table+"'"
                        tables_list.add(tab)
                    }
                    echo "$tables_list"
                }
            }
        }
    }
}
