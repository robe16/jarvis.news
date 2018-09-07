echo "Running Build ID: ${env.BUILD_ID}"

string serviceType  = "news"

docker_volumes      = ["-v /etc/ssl/certs:/etc/ssl/certs",
                      "-v ${params.fileConfig}:/jarvis/${serviceType}/config/config.json",
                      "-v ${params.folderLog}:/jarvis/${serviceType}/log/logfiles/"].join(" ")

deployLogin         = "${env.deploymentServerLogin_jarvisServer01}"

node {

    deleteDir()

    stage('checkout') {
        git "https://github.com/robe16/jarvis.${serviceType}.git"
    }
    //
    docker_img_name_build_id = "${params.serviceID}:${env.BUILD_ID}"
    docker_img_name_latest = "${params.serviceID}:latest"
    //
    stage('build') {
        //agent {
        //    docker {
        //        image 'resin/rpi-raspbian:latest'
        //    }
        //}
        try {sh "docker image rm ${docker_img_name_latest}"} catch (error) {}
        sh "docker build -t ${docker_img_name_build_id} ."
        sh "docker tag ${docker_img_name_build_id} ${docker_img_name_latest}"
    }
    //
    stage("deploy"){
        //
        String docker_img_tar = "docker_img.tar"
        //
        try {
            // remove any old tar files from cicd server
            sh "rm ~/${docker_img_tar}"
        } catch(error) {
            echo "No ${docker_img_tar} file to remove."
        }
        // create tar file of image
        sh "docker save -o ~/${docker_img_tar} ${docker_img_name_build_id}"
        // xfer tar to deploy server
        sh "scp -v -o StrictHostKeyChecking=no ~/${docker_img_tar} ${deployLogin}:~"
        // load tar into deploy server registry
        sh "ssh -o StrictHostKeyChecking=no ${deployLogin} \"docker load -i ~/${docker_img_tar}\""
        // remove the tar file from deploy server
        sh "ssh -o StrictHostKeyChecking=no ${deployLogin} \"rm ~/${docker_img_tar}\""
        // remove the tar file from cicd server
        sh "rm ~/${docker_img_tar}"
        // Set 'latest' tag to most recently created docker image
        sh "ssh -o StrictHostKeyChecking=no ${deployLogin} \"docker tag ${docker_img_name_build_id} ${docker_img_name_latest}\""
        //
    }
    //
    stage("start container"){
        // Stop existing container if running
        sh "ssh ${deployLogin} \"docker rm -f ${params.serviceID} && echo \"container ${params.serviceID} removed\" || echo \"container ${params.serviceID} does not exist\"\""
        // Start new container
        sh "ssh ${deployLogin} \"docker run --restart unless-stopped -e TZ=Europe/London -d ${docker_volumes} --net=host --name ${params.serviceID} ${docker_img_name_latest}\""
    }
}