# Register K8S cluster into ONAP
In order to register K8S cloud to ONAP you need to follow these steps:
  1. Prerequisite: K8S cluster has been created
  2. Copy **.kube/config** file and edit it any text editor.
  2.1 Remove certificate from cluster section (**certificate-authority-data**)
  2.2 Add **insecure-skip-tls-verify: true** to cluster section
  2.3 Edit server IP, replace internal IP with floating IP
  3. Copy and paste kubeconfig file to **config/kubeconfig**
