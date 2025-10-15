# End-to-End MLOps Pipeline Orchestration (Kubeflow, MLflow/DagsHub, Minikube)

This project showcases a complete MLOps workflow for a machine learning model, utilizing **Kubeflow Pipelines** for orchestration on a local **Minikube** cluster. **MLflow**, integrated with **DagsHub**, provides centralized experiment tracking and version control for reproducibility.

---

## 1. MLOps Toolchain Summary

| Tool | Category | Key Functionality |
| :--- | :--- | :--- |
| **Kubeflow Pipelines** | Orchestration | Automates the end-to-end ML workflow on Kubernetes. |
| **Minikube** | Infrastructure | Local single-node Kubernetes cluster for development. |
| **MLflow / DagsHub** | Tracking / Versioning | Remote experiment logging (metrics, parameters, artifacts) and code/data versioning. |
| **Docker** | Packaging | Containerization of the ML application for portability. |
| **GitHub** | Version Control | Source code management and integration with DagsHub. |

---

## 2. Infrastructure Setup (Minikube & Kubeflow)

The pipeline is deployed on a local Kubernetes environment.

### 2.1. Minikube and Kubectl Installation

1.  Ensure **Minikube** and **Kubectl** are installed and running:
    ```bash
    minikube start
    minikube status
    kubectl cluster-info
    ```

### 2.2. Kubeflow Deployment

1.  Set the desired Kubeflow Pipelines version:
    ```bash
    export PIPELINE_VERSION=2.14.3
    ```
2.  Apply the necessary Kubeflow manifests:
    ```bash
    kubectl apply -k "[github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION](https://github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION)"
    kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
    kubectl apply -k "[github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic?ref=$PIPELINE_VERSION](https://github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic?ref=$PIPELINE_VERSION)"
    ```
3.  Wait for all Kubeflow pods to be in the `Running` state:
    ```bash
    kubectl get pod -A
    ```
4.  Access the Kubeflow Dashboard locally:
    ```bash
    kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
    # Access: http://localhost:8080
    ```

---

## 3. Experiment Tracking (MLflow/DagsHub)

We use DagsHub as the remote MLflow Tracking Server to centralize all experiment results.

1.  **Repository Connection:** Ensure your DagsHub repository is linked to this GitHub project.
2.  **Authentication Setup:** Configure environment variables for remote MLflow tracking.

    ```bash
    # Get this URI from DagsHub (Remote -> Experiments)
    export MLFLOW_TRACKING_URI=[https://dagshub.com/](https://dagshub.com/)<YOUR_USER>/<YOUR_REPO_NAME>.mlflow
    export MLFLOW_TRACKING_USERNAME=<YOUR_DAGSHUB_USERNAME>
    # Use a DagsHub generated token for the password
    export MLFLOW_TRACKING_PASSWORD=<YOUR_DAGSHUB_TOKEN>
    ```
3.  The model training step within the Kubeflow pipeline includes **MLflow logging calls** that automatically send metrics, parameters, and the final model to this remote URI.

---

## 4. Application Containerization

The machine learning application is containerized for execution on the Kubernetes cluster.

1.  **Build Image:** Create the Docker image using the `Dockerfile` in the root directory:
    ```bash
    docker build -t mlops-project-09-app .
    ```
2.  **Login & Tag:** Authenticate with Docker Hub and tag the image:
    ```bash
    docker login
    docker tag mlops-project-09-app thilina9718/mlops-project-09-app:latest
    ```
3.  **Push to Registry:** Push the final image to Docker Hub, making it accessible to Kubeflow:
    ```bash
    docker push thilina9718/mlops-project-09-app:latest
    ```

---

## 5. Pipeline Development and Execution

The final stage involves defining the workflow and deploying it on Kubeflow.

1.  **Pipeline Definition:** The Kubeflow pipeline is defined in a Python script within the `kubeflow_pipeline` folder. This script references the Docker image pushed in Section 4.
2.  **Compile to YAML:** Run the Python script to generate the deployable YAML file:
    ```bash
    python kubeflow_pipeline/<your_pipeline_script_name>.py
    ```
3.  **Deploy and Run:**
    * Navigate to the **Kubeflow Dashboard** (`http://localhost:8080`).
    * Go to **Pipelines** $\to$ **Upload pipeline** and select the generated YAML file.
    * Create a **Run** under a new or existing **Experiment** to trigger the automated MLOps workflow.

### Verification

* **Kubeflow UI:** Monitor the pipeline's execution status, logs, and resource usage for each step.
* **DagsHub:** Review all logged metrics, parameters, and model artifacts in the **DagsHub Experiments** tab, confirming successful remote tracking.