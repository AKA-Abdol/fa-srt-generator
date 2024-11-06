@Library('jenkins-shared-libraries') _

pipeline {
    agent {
        kubernetes {
            inheritFrom 'base'
        }
    }
    environment {
        REGISTRY = 'r.glss.ir'
        STAGE = 'CI'
        BUILDKIT_PROGRESS = 'plain'
        BUILDX_LOG_LEVEL = 'warn'
        CONTAINER_LABEL = 'python'
        KUSTOMIZE_FASUB_NAME = 'fasub'
        KUSTOMIZE_FASUB_BACK_IMAGE = 'r.glss.ir/fasub/back'
        KUSTOMIZE_FASUB_DIR = 'fasub'
        KUSTOMIZE_REPO_URL = 'https://github.com/GolianGroup/deployments.git'
    }
    stages {
        stage('Checkout') {
            steps {
                script {
                    checkoutRepositories(scm, env.KUSTOMIZE_REPO_URL, env.KUSTOMIZE_FASUB_DIR)
                }
            }
        }
        stage('Prepare') {
            steps {
                script {
                    prepareEnvironment()
                    setupBuildx()
                }
            }
        }
        stage('Build and Push') {
            steps {
                container(env.CONTAINER_LABEL) {
                    script {
                        def fasubBackTags = []
                        
                        if (env.branchName == 'main') {
                            fasubBackTags = ["${env.KUSTOMIZE_FASUB_BACK_IMAGE}:main-${env.shortCommitHash}", "${env.KUSTOMIZE_FASUB_BACK_IMAGE}:main", "${env.KUSTOMIZE_FASUB_BACK_IMAGE}:latest"]
                        } else if (env.branchName == 'dev') {
                            fasubBackTags = ["${env.KUSTOMIZE_FASUB_BACK_IMAGE}:staging-${env.shortCommitHash}", "${env.KUSTOMIZE_FASUB_BACK_IMAGE}:staging", "${env.KUSTOMIZE_FASUB_BACK_IMAGE}:dev-${env.shortCommitHash}", "${env.KUSTOMIZE_FASUB_BACK_IMAGE}:dev"]
                        } else {
                            fasubBackTags = ["${env.KUSTOMIZE_FASUB_BACK_IMAGE}:${env.branchName}-${env.shortCommitHash}"]
                        }

                        def buildArgs = [
                            "FASUB_BACK_TAGS=${fasubBackTags.join(',')}"
                        ]
                        
                        buildxAndPush("Dockerfile", ".", buildArgs)
                        updateKustomizeImage(env.branchName, env.shortCommitHash, env.KUSTOMIZE_FASUB_NAME, env.KUSTOMIZE_FASUB_BACK_IMAGE, env.KUSTOMIZE_FASUB_DIR)
                    }
                }
            }
        }
    }
}
