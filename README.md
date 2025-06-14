# ✋ Bilingual Sign Language Recognition System (Arabic & English)

A full-stack, production-grade sign language recognition system using real-time webcam input, YOLOv8 deep learning models, and an automated CI/CD pipeline powered by Jenkins, Docker, Kubernetes, and Terraform.

---

## 🧠 Project Architecture

![System Architecture](architecture.jpg)

---

## 📁 Project Structure

```
Jenkins-pipeline/
├── arabic/                 # Arabic model service (Flask + YOLOv8)
├── english/                # English model service (Flask + YOLOv8)
├── frontend/               # Flask gateway + HTML UI
├── Jenkinsfile             # Jenkins pipeline stages
├── Kubernetes/             # YAML manifests for services and deployments
└── Terraform/              # IaC scripts for AWS infrastructure
```

---

## 🧠 Technical Overview

### 🔤 Dual YOLOv8 Inference Services
- Both `arabic/` and `english/` services load pre-trained `.pt` models using `ultralytics.YOLO`.
- Each model detects one sign per image with highest confidence.
- Outputs are returned via Flask APIs in real-time.

### 🌍 Frontend Service
- Flask app with `index.html` and JS-based webcam interface.
- Accepts captured image, converts to base64, and sends to the selected backend (Arabic or English).
- Receives prediction and displays it dynamically.

### 🔁 Communication Flow
- Services communicate via internal DNS in Kubernetes (`arabic-service`, `english-service`).
- Frontend uses `requests.post()` to call backend APIs with image data.

---

## 🚀 Jenkins CI/CD Pipeline

### Jenkins Setup
1. Deploy Jenkins using EC2 (manual or via Terraform).
2. Install required plugins:
   - Docker, Git, Pipeline, Kubernetes CLI
3. Add Jenkins credentials:
   - DockerHub login
   - AWS access key for Terraform

### Pipeline Stages (Defined in `Jenkinsfile`)
1. **Checkout**: Clones repo from GitHub.
2. **Unit Testing**: Runs model service tests (Flask endpoints).
3. **Docker Build**: Builds 3 images (Arabic, English, Frontend).
4. **Docker Push**: Pushes to DockerHub using Jenkins secrets.
5. **Kubernetes Deployment**: Applies K8s YAMLs to cluster.
6. **Notifications**: Logs output, optionally send Slack or email.

### Triggering the Pipeline
- Manual: Click "Build Now" in Jenkins UI.
- Automatic: GitHub webhook triggers on push.

---

## 🐳 Docker Services

Each microservice has its own `Dockerfile`.

### Example (Arabic):
```bash
docker build -t arabic-sign-api ./arabic
docker run -p 5051:5051 arabic-sign-api
```

---

## ☸️ Kubernetes Deployment

Manifests included for:
- `arabic-service` and `english-service`: Expose model APIs
- `frontend-service`: Serves UI
- Each has its own Deployment and ClusterIP Service

```bash
kubectl apply -f Kubernetes/
```

Access via:

```bash
minikube service frontend-service
# OR
kubectl get svc frontend-service
```

---

## ☁️ Infrastructure with Terraform

Terraform files provision:

- Jenkins EC2 instance
- Security groups, key pairs, subnets
- Optional EKS cluster (Kubernetes)

### To Deploy:
```bash
cd Terraform/
terraform init
terraform apply
```

Backend state can be stored in S3 (configured in `backend.tf`).

---

## 🔧 Config & Environment

- Flask backend services support env overrides:
  - `ARABIC_SERVICE_HOST`
  - `ENGLISH_SERVICE_HOST`
- These map to Kubernetes internal service names.

---

## 📋 Requirements

| Tool        | Version |
|-------------|---------|
| Python      | ≥ 3.8   |
| Docker      | Latest  |
| Terraform   | ≥ 1.0   |
| Jenkins     | LTS     |
| Kubernetes  | Any     |
| Ultralytics | YOLOv8  |

---

## 👨‍💻 Maintainer

[Yussuf Yasser](https://github.com/yussufyasser)

---

## 🧪 Future Improvements

- [ ] Ingress with NGINX and TLS
- [ ] Model versioning via S3
- [ ] Monitoring: Prometheus + Grafana
- [ ] Centralized logging (e.g., ELK stack)
