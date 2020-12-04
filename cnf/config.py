from uuid import uuid4


class Config:
    #### REGION DETAILS ####
    COMPLEX_ID = "complex"
    CLOUD_OWNER = "k8sCloudOwner"
    CLOUD_REGION = "k8s-region-1"  # Fill
    AVAILABILITY_ZONE_NAME = "k8s-availability-zone"
    HYPERVISOR_TYPE = "k8s"
    TENANT_NAME = "k8s-tenant-1"  # Fill

    CLUSTER_KUBECONFIG_PATH = "artifacts/cluster_kubeconfig"  # Add kubeconfg
    ONAP_KUBECONFIG_PATH = "artifacts/onap_kubeconfig"  # Add kubeconfg

    #### SERVICE DETAILS ####
    GLOBAL_CUSTOMER_ID = "customer_CNF"  # Fill
    VSPFILE = "vsp/vfw_k8s_demo.zip"  # Fill
    VENDOR = "vendor_CNF"  # Fill
    SERVICENAME = "vfw_k8s_demo_CNF"  # Fill
    VSPNAME = "VSP_" + SERVICENAME
    VFNAME = "VF_" + SERVICENAME
    SERVICE_INSTANCE_NAME = "INSTANCE_" + SERVICENAME
    SDNC_ARTIFACT_NAME = "vnf"

    # Fill the vf-module list with vf module labels, profiles and namespaces names
    VF_MODULE_LIST = {"base_template":
                          {"name": "base_template",
                           "k8s-rb-profile-name": "vfw-cnf-cds-base-profile",
                           "k8s-rb-profile-namespace": "vfirewall"},
                      "vfw":
                          {"name": "vfw",
                           "k8s-rb-profile-name": "vfw-cnf-cds-base-profile",
                           "k8s-rb-profile-namespace": "vfirewall"},
                      "vpkg":
                          {"name": "vpkg",
                           "k8s-rb-profile-name": "vfw-cnf-cds-base-profile",
                           "k8s-rb-profile-namespace": "vfirewall"},
                      "vsn":
                          {"name": "vsn",
                           "k8s-rb-profile-name": "vfw-cnf-cds-base-profile",
                           "k8s-rb-profile-namespace": "vfirewall"}}

    ######## DEFAULT VALUES ########
    OWNING_ENTITY = "OE-Demonstration"
    PROJECT = "Project-Demonstration"
    PLATFORM = "test"
    LINE_OF_BUSINESS = "LOB-Demonstration"
