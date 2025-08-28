# Kubernetes Manifests — Complete Set

This repo is a curated collection of Kubernetes YAML manifests, designed to show most of the common resource types:  
Pods, Services, Controllers, RBAC, Namespaces, Network Policies, Certs, and KIND cluster configs.  

It’s a great starting point for learning, testing, or demoing Kubernetes.

---

## 📂 What’s Inside

### 🏗 Cluster Setup
- **`kind.yml`**, **`kind-calico.yml`**, **`kind-CNI.yml`**, **`kind-for-network-policy.yml`** → KIND cluster configs with different CNIs / networking modes.  
- **`cluster.yml`** → Cluster-level configuration.  
- **`k-config.yml`** → Example kubeconfig object (used for alternate contexts).  

### 🔹 Workloads & Controllers
- **`pod.yml`**, **`pod-myapp.yml`**, **`pod-new.yml`** → Pod manifests for different apps.  
- **`newnginx.yml`** → Nginx Deployment.  
- **`redis.yml`** → Redis pod/deployment.  
- **`rc.yml`** → ReplicaController (older style, useful for learning).  
- **`ds.yml`** → DaemonSet to run pods on every node.  

### 🔹 Services
- **`clusterip.yml`** → ClusterIP service (internal).  
- **`nodeport.yml`** → NodePort service (exposed via node IP).  
- **`lb.yml`** → LoadBalancer service (cloud-exposed).  

### 🔹 Namespaces & Networking
- **`ns.yml`** → Custom Namespace.  
- **`net-policy.yml`** → NetworkPolicy for pod-to-pod traffic restrictions.  

### 🔹 Certificates & Security
- **`csr.yml`** → CertificateSigningRequest.  
- **`issuecert.yml`** → Issuer + Certificate (cert-manager).  

### 🔹 RBAC (Access Control)
- **`role.yml`** → Role with namespace-scoped permissions.  
- **`role-binding.yml`** → Binds Role to a ServiceAccount or User.  

---

## How to Use

### 1. Create a KIND Cluster
```bash
kind create cluster --config kind.yml

2. Deploy Workloads

kubectl apply -f pod.yml
kubectl apply -f newnginx.yml
kubectl apply -f redis.yml

3. Expose Them

kubectl apply -f clusterip.yml
kubectl apply -f nodeport.yml
kubectl apply -f lb.yml

4. Add Controllers

kubectl apply -f rc.yml
kubectl apply -f ds.yml

5. Namespace & Policies

kubectl apply -f ns.yml
kubectl apply -f net-policy.yml

6. RBAC

kubectl apply -f role.yml
kubectl apply -f role-binding.yml

7. Certificates

kubectl apply -f csr.yml
kubectl certificate approve <csr-name>
kubectl apply -f issuecert.yml

