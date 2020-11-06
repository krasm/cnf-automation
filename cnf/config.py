#### REGION DETAILS ####
from uuid import uuid4

COMPLEX_ID = "complex"
CLOUD_OWNER = "k8sCloudOwner"
CLOUD_REGION = "k8s-region-2"
AVAILABILITY_ZONE_NAME = "k8s-availability-zone"
HYPERVISOR_TYPE = "k8s"
TENANT_NAME = "k8s-tenant-1"

CLUSTER_KUBECONFIG_PATH = "artifacts/cluster_kubeconfig"
ONAP_KUBECONFIG_PATH = "artifacts/onap_kubeconfig"

#### SERVICE DETAILS ####
GLOBAL_CUSTOMER_ID = "Michal_customer"
VSPFILE = "vsp/vfw_k8s_demo.zip"
VENDOR = "Michal_vendor"
SERVICENAME = "vfw_k8s_demo_CNF"
VSPNAME = "VSP_" + SERVICENAME
VFNAME = "VF_" + SERVICENAME
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
PROFILE_NAME = "vfw-cnf-cds-base-profile"
SERVICE_INSTANCE_NAME = "INSTANCE_" + SERVICENAME + str(uuid4())

SDNC_ARTIFACT_NAME = "vnf"
SDNC_MODEL_NAME = "vFW_CNF_CDS"  # used only for instantiation
SDNC_MODEL_VERSION = "7.0.0"  # used only for instantiation

######## DEFAULT VALUES ########
OWNING_ENTITY = "OE-Demonstration"
PROJECT = "Project-Demonstration"
PLATFORM = "test"
LINE_OF_BUSINESS = "LOB-Demonstration"

