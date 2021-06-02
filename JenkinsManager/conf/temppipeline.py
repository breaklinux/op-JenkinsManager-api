jenkinFileBody = """
#!groovy
import groovy.transform.Field
import groovy.json.JsonOutput
import groovy.json.JsonSlurperClassic
@Field CHANGE_HOST = 'http://192.168.54.12'
@Field CONSOLE_SCRIPT = "/chj/data/jenkins-data"
@Field SERVICE_TYPE = "ChangE"

try {
    node {
        parameters {
            string(defaultValue: 'type', description: '构建应用类型 1.java 2.python 3.go 4.node.js', name: 'type')
            string(defaultValue: 'gitURL', description: 'git地址', name: 'gitURL')
        }
        stage('checkout') {
            try {
                checkout([$class: 'GitSCM', branches: [[name: '${branch}']], doGenerateSubmoduleConfigurations: false, userRemoteConfigs: [[credentialsId: 'cd_change_jenkins', url: '${giturl}']]])
            } catch (Exception e) {
                print(e)
            }
        }
        stage('Build') {
            //构建类型为1 属于java 类型应用
            //构建类型为2 属于python 类型应用
            //构建类型为3 属于go 类型应用
            //构建类型为4 属于node 类型应用
            try {
                if ("$type" == "1") {
                    sh "mvn clean package -U -DskipTests=true"
                } else if ("$type" == "2") {
                   sh "echo '不需要编译'"

                } else if ("$type" == "3") {
                    sh "go build"

                } else if ("$type" == "4") {
                    sh "rm -rf  dist"
                    sh "cnpm install"
                }
            }catch (Exception e) {
                print(e)
            }
    }
    }
    } catch (Exception e ) {
        print(e)
    }
"""
