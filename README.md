# ✋ Bilingual Sign Language Recognition System (Arabic & English)

A full-stack, production-grade sign language recognition system using real-time image input, YOLOv8 deep learning models, and a robust CI/CD & deployment pipeline powered by Jenkins, Docker, Kubernetes, and Terraform.

---

## 🧠 Project Architecture

```
                        +-----------------------+
                        |      End User         |
                        |  (Webcam Interface)   |
                        +-----------+-----------+
                                    |
                                    v
                        +-----------+-----------+
                        |       Frontend        |
                        | Flask + index.html UI |
                        +-----------+-----------+
                                    |
           +------------------------+------------------------+
           |                                                 |
           v                                                 v
+-------------------------+                      +-------------------------+
|     Arabic Model API    |                      |    English Model API    |
| Flask + YOLOv8 + Docker |                      | Flask + YOLOv8 + Docker |
+-------------------------+                      +-------------------------+
           |                                                 |
           +------------------------+------------------------+
                                    v
                            +---------------+
                            | Kubernetes     |
                            | Services & DNS |
                            +-------+-------+
                                    |
                                    v
                            +---------------+
                            |  Jenkins CI/CD|
                            |  + Terraform  |
                            +---------------+
```

---

## 📁 Project Structure

```
Jenkins-pipeline/
├── arabic/                 # Arabic model service (Flask + YOLO)
├── english/                # English model service (Flask + YOLO)
├── frontend/               # Web UI + gateway Flask app
├── Jenkinsfile             # CI/CD pipeline definition
├── Kubernetes/             # Kubernetes manifests for all services
└── Terraform/              # Terraform infra provisioning scripts
```

---

## 🚀 How to Run via Jenkins CI/CD

### Jenkins Setup

1. **Install Jenkins** (or launch via Terraform on EC2).
2. **Install Plugins**:
   - Docker
   - Pipeline
   - Kubernetes CLI
   - Git
3. **Configure Credentials**:
   - DockerHub username/password
   - AWS CLI for `terraform apply`

### Pipeline Flow (from Jenkinsfile)

1. **SCM Checkout** – Pulls this repo.
2. **Testing** – Runs unit tests for Arabic and English model services.
3. **Docker Build** – Builds Docker images for all services.
4. **Push Images** – Pushes to DockerHub using your credentials.
5. **Deploy to Kubernetes** – Uses `kubectl apply` to deploy the system.
6. **Post-build info** – Shows deployment logs or URLs.

### Triggering the Pipeline

- Manual: Run pipeline from Jenkins UI
- Auto: Set GitHub webhook on push to `main`/`master`

---

## 📦 Backend Services

**Arabic**
- Endpoint: `/arabic_sign` (port 5051)

**English**
- Endpoint: `/english_sign` (port 5052)

Both return predicted characters based on YOLOv8 detection.

---

## 🌐 Frontend UI

- Flask app with HTML interface (`index.html`)
- Communicates with Arabic or English service based on dropdown selection
- Displays prediction output directly to the user

---

## ☸️ Kubernetes Deployment

All services are deployed to Kubernetes via:

```bash
kubectl apply -f Kubernetes/
```

---

## ☁️ Terraform Infrastructure

Run in `Terraform/`:

```bash
terraform init
terraform apply
```

This can provision:
- Jenkins EC2
- Kubernetes cluster (EKS-ready)
- Security groups, key pairs, networking

---

## 🛠️ Requirements

- Python ≥ 3.8
- Docker & DockerHub
- Kubernetes cluster or Minikube
- Terraform CLI
- Jenkins server




