pipeline {
    
    agent any
    
    stages{
        stage("run shell file"){
            steps{
                withCredentials([usernamePassword(credentialsId: 'mol-dev', passwordVariable: 'pass', usernameVariable: 'user')]) {
                // some block
                sh """
                    #!/bin/bash
                    cd jenkins
                    ./*.sh
                """
                }
            }
        }
    }
}
