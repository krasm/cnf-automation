#### REGION DETAILS ####
from uuid import uuid4

COMPLEX_ID = "complex"
CLOUD_OWNER = "k8sCloudOwner"
CLOUD_REGION = "k8s-region-bcom-1"
AVAILABILITY_ZONE_NAME = "k8s-availability-zone"
HYPERVISOR_TYPE = "k8s"
TENANT_NAME = "k8s-tenant-bcom-1"
NAMESPACE_NAME = "bcom"

CLUSTER_KUBECONFIG_PATH = "artifacts/cluster_kubeconfig"
ONAP_KUBECONFIG_PATH = "artifacts/onap_kubeconfig"

#### SERVICE DETAILS ####
GLOBAL_CUSTOMER_ID = "Michal_customer"
VSPFILE = "vsp/wef-3.0_CNF.zip"
VENDOR = "Michal_vendor"
SERVICENAME = "wef-3-0_CNF"
VSPNAME = "VSP_" + SERVICENAME
VFNAME = "VF_" + SERVICENAME
VF_MODULE_LIST = ["wef-3-0"]
SERVICE_INSTANCE_NAME = "INSTANCE_" + SERVICENAME + str(uuid4())

SDNC_ARTIFACT_NAME = "vnf"
SDNC_MODEL_NAME = "HELM_CBA"  # used only for instantiation
SDNC_MODEL_VERSION = "1.0.0"  # used only for instantiation
PROFILE_NAME = "wef-cnf-cds-base-profile"

######## DEFAULT VALUES ########
OWNING_ENTITY = "OE-Demonstration"
PROJECT = "Project-Demonstration"
PLATFORM = "test"
LINE_OF_BUSINESS = "LOB-Demonstration"

