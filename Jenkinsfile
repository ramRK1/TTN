pipeline {
    
    agent any
    
    stages{
        stage("run shell file"){
            steps{
                withCredentials([usernamePassword(credentialsId: 'mol-dev', passwordVariable: 'pass', usernameVariable: 'user')]) {
                // some block
                sh """
                    echo $user
                    echo $pass
                """
                }
            }
        }
    }
}
