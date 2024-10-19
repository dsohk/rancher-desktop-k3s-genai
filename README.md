# Introduction - Develop & Deploy GenAI App with Ollama, Open WebUI with K3S in Rancher Desktop

In this session, we're diving into an exciting lineup of tools and technologies to empower your development and deployment processes. 

**Rancher Desktop with K3s**: Rancher Desktop is an open-source application developed by SUSE that brings Kubernetes and container management to your desktop, we'll set up a local Kubernetes environment using Rancher Desktop and K3s. This setup will simulate a production-like environment, enabling you to test and refine your deployments effectively.

**OpenWebUI with Ollama**: OpenWebUI is a application with an intuitive interface that provides GenAI capabilities, we'll explore how to use Mistral LLM with API to enhances your application development by integrating GenAI advanced functionalities and insights, making the application smarter and more intuitive. 

**OpenDGR API Gateway**: OpenDGR is an open-source application developed by TPI Software is an API gateway and management solution designed to act as an intermediary between client applications and backend services. It provides a range of features to manage and secure API traffic, ensuring efficient communication and data flow.

**Rancher Fleet**: Rancher Fleet is a Continuous Delivery (GitOps) tool to manage deployments from a single Kubernetes cluster to large-scale deployment of multiple Kubernetes clusters. We'll deploy our GenAI applications to multi cluster environment using Rancher Fleet to automate and manage large-scale deployments, ensuring consistency and reliability across your infrastructure.

By the end of this workshop, you'll have a comprehensive understanding of these tools and how they can streamline your development workflow from local testing to production deployment. Let's get started and make the most of this collaborative learning experience!


## Table of Contents:

* Task 1 - Setup Rancher Desktop and K3S
* Task 2 - Deploy GenAI app OpenWebUI with Ollama into Rancher Desktop local K3s cluster
* Task 3 - Deploy the OpenDGR API gateway protec the GenAI app
* Task 4 - Multi-Cluster Deployment with Rancher Fleet  


## System Requirements

To complete this lab, you need to have a laptop (Quad core, 16GB RAM and 50GB free SSD disk space) with fast and stable internet access with one of the following operating systems installed.

* Windows 10, 
* MacBook Apple Silicon M1 or above, or 
* Linux (e.g. OpenSUSE Leap)



## Task 1 - Setup Rancher Desktop and K3S

Setup the development environment. Intend to develop everything within containers.


Get K3S and [Rancher Desktop](https://rancherdesktop.io/) up and running

1. Download from [Rancher Desktop](https://rancherdesktop.io/) website and install the latest stable version of Rancher Desktop application (v1.16 at the time of this writing) on your laptop.

2. Configure VM used by Rancher Desktop (Under Preferences, Virtual Machine tab) to be 10GB RAM and 4 vcore

![01-rancher-desktop-preference](assets/01-rancher-desktop-preference.png)

3. Configure Container Engine used by Rancher Desktop (Under Preferences, Container Engine tab) to dockerd(moby)

![01-rancher-desktop-container-engine](assets/01-rancher-desktop-container-engine.png)

4. Configure Kubernetes Version used by Rancher Desktop (Under Preferences, Kubernetes tab) to v1.28.5

![01-rancher-desktop-container-engine](assets/01-rancher-desktop-k8s-version.png)

5. Enable resource monitoring by navigating to Extensions and Install Resource usage.

![01-rancher-desktop-extension-install-resource-usage](assets/01-rancher-desktop-extension-install-resource-usage.png)

5. Check Resource usage dashboard by navigating to Resource usage
![01-rancher-desktop-resource-usage](assets/01-rancher-desktop-resource-usage.png)

6. After the Kubernetes services (k3s) is up and running, we can open a terminal console to access to the cluster.
   Open your terminal, you should now have access to your local K3S cluster.

```
❯ kubectl get node
NAME                   STATUS   ROLES                  AGE   VERSION
lima-rancher-desktop   Ready    control-plane,master   76d   v1.28.5+k3s1
```


## Task 2 - Deploy GenAI app Open WebUI with Ollama into Rancher Desktop local K3s cluster

Let's deploy GenAI app Open WebUI with ollama into our local k3s cluster.

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
  models: ["mistral:7b"]
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
  --values open-webui-values-k3s.yaml
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
service/open-webui-ollama      ClusterIP   10.43.94.196   <none>        11434/TCP      7d

NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/open-webui-pipelines   1/1     1            1           7d
deployment.apps/open-webui-ollama      1/1     1            1           7d

NAME                                            DESIRED   CURRENT   READY   AGE
replicaset.apps/open-webui-pipelines-bd86b5bc   1         1         1       7d
replicaset.apps/open-webui-ollama-5d6b97fc9f    1         1         1       7d

NAME                          READY   AGE
statefulset.apps/open-webui   1/1     7d
```


5. Enable port-forwarding for open-webui , open-webui-ollama and open-dgr-svc by navigating to Port Forwarding.
   * forward `open-webui` to port `8080`
   * forward `open-webui-ollama` to port `11434`

![02-rancher-desktop-port-forwarding-1](assets/02-rancher-desktop-port-forwarding-1.png)


6. Navigate to the `http://127.0.0.1:8080` and sign up your own first user account and sign in.

![02-openwebui-1](assets/02-openwebui-1.png)


7. Download the `mistral` LLM from Open WebUI.

![02-openwebui-2](assets/02-openwebui-2.png)


8. Let's try to ask questions to see if the local LLM works.
   For example: `why is the sky blue?  please answer in less than 10 words`

![02-openwebui-3](assets/02-openwebui-3.png)

9. Let's try test the ollama api with command curl
```
curl http://127.0.0.1:11434/api/chat -d '
{
  "model": "mistral",
  "stream": false,
  "messages": [
    { "role": "user", "content": "why is the sky blue?  please answer in less than 10 words." }
  ]
} '
```

## Task 3 - Deploy the OpenDGR API gateway protec the GenAI app

Let's deploy OpenDGR onto our local k3s cluster for securing the GenAI apps access.

1.  OpenDGR Deployment with a single line curl command 
```
curl -s https://raw.githubusercontent.com/TPIsoftwareOSPO/digiRunner_Open/refs/heads/master/manifest/open_dgr.yaml | kubectl apply -f -
```

2. Enable port-forwarding for open-webui , open-webui-ollama and open-dgr-svc by navigating to Port Forwarding.
   * forward `open-dgr-svc` to port `18080`

   ![image-20241016205503](assets/03-rancher-desktop-port-forwarding-2.png)

3. Navigate to the `http://127.0.0.1:18080/dgrv4/ac4/login` and login with OpenDGR manager.
* 登入帳號: manager
* 密碼: manager123
![03-opendgrui-login](assets/03-opendgrui-login.png) 

4. Check the ollama API service internal cluster IP
```
❯ kubectl get svc -n myfirstgenai

NAME                           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/open-webui             NodePort    10.43.110.192   <none>        80:32574/TCP   7d
service/open-webui-pipelines   ClusterIP   10.43.231.90    <none>        9099/TCP       7d
service/open-webui-ollama      ClusterIP   10.43.94.196   <none>        11434/TCP      7d

```

5.  Navigate to API registry (Under API Management, API Registry).
* Target URL : http://<service/open-webui-ollama-clusterIP>:11434/api/chat # replace with the ollama API service internal cluster IP above
* API Name : chat
* digiRunner Proxy Path : chat
* Http Methods : POST
* No Auth : Yes
![03-opendgrui-dashboard](assets/03-opendgrui-api-registry.png)  


6.  Navigate to API List, Enable Chat API.
![03-opendgrui-api-list](assets/03-opendgrui-api-list.png)  

7.  Navigate to API Test and try test the ollama api

* Target URL : http://localhost:18080/chat
* Http Methods : POST
* Http body:
```
{
  "model": "mistral",
  "stream": false,
  "messages": [
    { "role": "user", "content": "why is the sky blue?  please answer in less than 10 words." }
  ]
} 
```
![03-opendgrui-api-test](assets/03-opendgrui-api-test.png)

8. API test result with ollama.
![image-20241015160909483](assets/03-opendgrui-ollama-api-test.png)  

## Task 4 - Multi-Cluster Deployment with Rancher Fleet (Demo steps)

The GenAI app works great! but the steps to manual deploy and update multiple clusters are too time consuming. Lets adopt the GitOps approach to maintain the GenAI app.


1. Go to Rancher Server home page, Click the top left `☰` 3-line bar icon to expand the navigation menu, click `Continuous Delivery`

![rancher-fleet-homepage](assets/04-rancher-fleet-homepage.png)

Before we proced, let's verify if we can see all our clusters in Continous Delivery

![rancher-fleet-cluster-list](assets/04-rancher-fleet-cluster-list.png)

With Rancher Fleet, one can manage individual or group of clusters. Managing cluster via Group reduces adminstrative efforts. 


1. Now we will create a Cluster Group.

Navigate to `Cluster Group` and click on `Create`. 

![rancher-fleet-cluster-group-create](assets/04-rancher-fleet-cluster-group-create.png)

Give it a name `development`

Under Cluster Selector , click **Add Rule** provide the following values

Key:`env`

Operator: `in list`

Value:`dev` 

we are going to use the same Label which was used to create `azure-rke2-cluster` and `aliyun-rke2-cluster`.

![rancher-fleet-cluster-group-dev](assets/04-rancher-fleet-cluster-group-dev.png)
 
Once you key in the key:value pair, Rancher will use the selector labels to indentify the clusters to be associated with our newly created cluster group in Rancher Continuous Delivery. You should see it show matches all 2 existing clusters. 

Click on `Create` which will create our first Cluster Group.

![rancher-fleet-cluster-group-added](assets/04-rancher-fleet-cluster-group-added.png)

we can click into the `development` cluster group for resources details.

![rancher-fleet-cluster-group-details](assets/04-rancher-fleet-cluster-group-details.png)


1. Configure a git repository

we will use the fleet-examples git repo to deploy the Kubernetes sample guestbook application. The app will be deployed into the default namespace.

you can also fork the fleet-examples Git Repository(https://github.com/rancher/fleet-examples) for testing.

In the `Git Repos` page click on `Add Repository`

![rancher-fleet-git-repo-add](assets/04-rancher-fleet-git-repo-add.png)

- Enter `fleet-examples` as your git repo `Name`
- Enter `https://github.com/rancher/fleet-examples` (the fleet-examples git repo URL) in `Repository URL`  

- scroll to the bottom and enter Paths: `simple` , with all the parameters default setting then click **Next**

Sample output of the GitRepo configuration below

![rancher-fleet-git-repo-add-details](assets/04-rancher-fleet-git-repo-add-details.png)

in the Step2, Deploy to `Target` dropdown list, select the Cluster Group we created previosuly `development`. 


![rancher-fleet-git-repo-add-details-step2](assets/04-rancher-fleet-git-repo-add-details-step2.png)


We have successfully completed Rancher Contious Delivery (GitOps) configuration. 

![rancher-fleet-git-repo-list](assets/04-rancher-fleet-git-repo-list.png)

click into the `fleet-examples` git repo, you can expect the example app will be deployed to the cluster group in a minute.

![rancher-fleet-git-repo-status](assets/04-rancher-fleet-git-repo-status.png)

When there is any commit or updates in the git repo, fleet by default will checks the git repo changes every 15 seconds, then fleet will deploy new changes into the cluster group automatically.


## Conclusion

We successfully set up a Rancher Desktop with K3s to create a local Kubernetes environment. Next, we deployed the GenAI application, OpenWebUI with Ollama, into the local K3s cluster. Finally, we secured the GenAI app using the OpenDGR API gateway. 

As the next step, we will demo to utilize Rancher Fleet to deploy the GenAI applications into the production environment, ensuring scalability and reliability

By following these steps, users can effectively simulate a production environment, test deployments, and manage large-scale applications.


