# Develop & Deploy GenAI App with Ollama, Open WebUI with K3S in Rancher Desktop

In this guide, we are going to show you how to ...



Table of Contents:

[TOC]

## System Requirements

To complete this lab, you need to have a laptop (Quad core, 16GB RAM and 50GB free SSD disk space) with fast and stable internet access with one of the following operating systems installed.

* Windows 10, 
* MacBook Apple Silicon M1 or above, or 
* Linux (e.g. OpenSUSE Leap)



## Setup Rancher Desktop and K3S

Setup the development environment. Intend to develop everything within containers.



Get K3S and [Rancher Desktop](https://rancherdesktop.io/) up and running

1. Download from [Rancher Desktop](https://rancherdesktop.io/) website and install the latest stable version of Rancher Desktop application (v1.16 at the time of this writing) on your laptop.

2. Configure VM used by Rancher Desktop (Under Preferences, Virtual Machine tab) to be 10GB RAM and 4 vcore

   ![image-20241014145426836](/Users/derekso_1/Work/suse-hands-on-workshops/rancher-desktop-k3s-genai/assets/01-rancher-desktop-preference.png)

3. Enable resource monitoring  by navigating to Extensions and Install Resource usage.

   ![image-20241014221056849](/Users/derekso_1/Work/suse-hands-on-workshops/rancher-desktop-k3s-genai/assets/02-rancher-desktop-resource-usage.png)

   

4. After the Kubernetes services (k3s) is up and running, we can open a terminal console to access to the cluster.

5. Open your terminal, you should now have access to your local K3S cluster.

```
❯ kubectl get node
NAME                   STATUS   ROLES                  AGE   VERSION
lima-rancher-desktop   Ready    control-plane,master   41d   v1.21.14+k3s1
```





## Deploy Ollama and OpenWebUI onto local K3S

Let's deploy Ollama and Open WebUI onto our local k3s cluster.



1. Prepare the `open-webui-values-k3s.yaml` file.

```
ollama:
  image:
    tag: 0.3.9
  resources:
    requests:
      cpu: "2000m"
      memory: "2Gi"
    limits:
      cpu: "4000m"
      memory: "6Gi"
      nvidia.com/gpu: "0"
  service:
    type: ClusterIP
  gpu:
    enabled: false
  persistentVolume:
    enabled: true
    size: 20Gi

resources:
  requests:
    cpu: "500m"
    memory: "500Mi"
  limits:
    cpu: "1000m"
    memory: "1Gi"
ingress:
  enabled: true
  host: open-webui.example.com
service:
  type: NodePort
```



2. Add helm repo for Open WebUI.

```
helm repo add open-webui https://helm.openwebui.com/
helm repo update
```



3. Deploy open-webui with embedded llama onto your local k3s

```
kubectl create ns myfirstgenai
helm upgrade --install open-webui-ollama open-webui/open-webui \
  --namespace myfirstgenai \
  --create-namespace \
  --values open-webui-values.yaml
```



4. Check the deployment status

```
❯ kubectl get all -n myfirstgenai
NAME                                      READY   STATUS    RESTARTS   AGE
pod/open-webui-pipelines-bd86b5bc-nzpvb   1/1     Running   0          7d
pod/open-webui-0                          1/1     Running   0          7d
pod/open-webui-ollama-5d6b97fc9f-kjzqw    1/1     Running   0          7d

NAME                           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/open-webui             NodePort    10.43.110.192   <none>        80:32574/TCP   7d
service/open-webui-pipelines   ClusterIP   10.43.231.90    <none>        9099/TCP       7d
service/open-webui-ollama      ClusterIP   10.43.152.145   <none>        11434/TCP      7d

NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/open-webui-pipelines   1/1     1            1           7d
deployment.apps/open-webui-ollama      1/1     1            1           7d

NAME                                            DESIRED   CURRENT   READY   AGE
replicaset.apps/open-webui-pipelines-bd86b5bc   1         1         1       7d
replicaset.apps/open-webui-ollama-5d6b97fc9f    1         1         1       7d

NAME                          READY   AGE
statefulset.apps/open-webui   1/1     7d
```



5. The open webui is accessible via your localhost. Let's define the local DNS entry (e.g. `/etc/hosts` file) in our laptop.

```
192.168.64.2 	open-webui.example.com
```



6. Navigate to the `open-webui.example.com` and sign up your own first user account and sign in.

![image-20241015160909483](/Users/derekso_1/Work/suse-hands-on-workshops/rancher-desktop-k3s-genai/assets/03-openwebui-1.png)



7. Download the `mistral` LLM from Open WebUI.

![image-20241015162104492](/Users/derekso_1/Work/suse-hands-on-workshops/rancher-desktop-k3s-genai/assets/03-openwebui-2.png)



8. Let's try to ask questions to see if the local LLM works.

![image-20241015162530225](/Users/derekso_1/Work/suse-hands-on-workshops/rancher-desktop-k3s-genai/assets/03-openwebui-3.png)



## Deploy the GenAI app to Rancher-managed environment

TBD - Using GitOps / Fleet or ArgoCD approach




