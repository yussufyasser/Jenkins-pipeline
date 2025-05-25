pipeline {
    agent any

    environment {
        TF_DIR = "${WORKSPACE}/Terraform"
        KUBE_DIR = "${WORKSPACE}/Kubernetes"

        APP_NAME = "jenkins-pipeline-app"
        GIT_REPO = "https://github.com/yussufyasser/Jenkins-pipeline.git"
        GIT_PATH = "Kubernetes"
        DEST_NAMESPACE = "default"
        ARGO_NAMESPACE = "argocd"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/yussufyasser/Jenkins-pipeline.git'
            }
        }

    
stage('Configure AWS Credentials') {
    steps {
        withCredentials([
            string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
            string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
        ]) {
            sh '''
mkdir -p ~/.aws
cat > ~/.aws/credentials <<EOF
[default]
aws_access_key_id = $AWS_ACCESS_KEY_ID
aws_secret_access_key = $AWS_SECRET_ACCESS_KEY
EOF
'''
        }
    }
}



        stage('Terraform Init & Apply') {
            steps {
                dir(env.TF_DIR) {
                    sh 'aws sts get-caller-identity'

                    sh 'terraform init'
                    sh 'terraform apply -auto-approve'
                }
            }
        }

        stage('Apply Kubernetes Manifests') {
            steps {
                dir(env.KUBE_DIR) {
                    sh 'aws eks update-kubeconfig --name my-sign-recognition-cluster --region us-east-1'
                    sh 'kubectl apply -f .'
                    sh 'kubectl create namespace argocd || true'
                    sh 'kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml'
                }
            }
        }

        stage('Wait for Argo CD Pods') {
            steps {
                sh '''
                echo "Waiting for Argo CD to be ready..."

                # Wait up to 6 minutes total, checking every 30 seconds
                for i in {1..12}; do
                    NOT_READY=$(kubectl get pods -n argocd --field-selector=status.phase!=Running -o name)
                    if [ -z "$NOT_READY" ]; then
                        echo "All Argo CD pods are running!"
                        exit 0
                    fi
                    echo "Still waiting for Argo CD pods to be ready..."
                    sleep 30
                done

                echo "Timeout waiting for Argo CD pods."
                kubectl get pods -n argocd
                exit 1
                '''
            }
        }


        stage('ArgoCD App Deployment') {
            steps {
                script {
                    sh '''
                    set -e

                    echo "Fetching Argo CD initial admin password..."
                    ARGOCD_PASSWORD=$(kubectl -n $ARGO_NAMESPACE get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
                    ARGOCD_SERVER=$(kubectl -n $ARGO_NAMESPACE get svc argocd-server -o jsonpath="{.status.loadBalancer.ingress[0].hostname}")

                    if [ -z "$ARGOCD_SERVER" ]; then
                      echo "No LoadBalancer found, using port-forward on localhost..."
                      kubectl port-forward svc/argocd-server -n $ARGO_NAMESPACE 8080:443 &
                      sleep 5
                      ARGOCD_SERVER="localhost:8080"
                    fi

                    echo "Logging into Argo CD server $ARGOCD_SERVER ..."
                    argocd login $ARGOCD_SERVER --username admin --password $ARGOCD_PASSWORD --insecure

                    echo "Creating Argo CD app $APP_NAME ..."
                    argocd app create $APP_NAME \
                      --repo $GIT_REPO \
                      --path $GIT_PATH \
                      --dest-server https://kubernetes.default.svc \
                      --dest-namespace $DEST_NAMESPACE \
                      --sync-policy automated || true  # allow failure if app already exists

                    echo "Syncing Argo CD app $APP_NAME ..."
                    argocd app sync $APP_NAME
                    '''
                }
            }
        }
    }
}
