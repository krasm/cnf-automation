import logging
import os
from uuid import uuid4

from config import *
from so_db_adapter import SoDBAdapter
from onapsdk.aai.business import Customer
from onapsdk.aai.cloud_infrastructure import Complex, CloudRegion
from onapsdk.msb.k8s import ConnectivityInfo

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
fh = logging.StreamHandler()
fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)

MYPATH = os.path.dirname(os.path.realpath(__file__))

#### Create complex if not exists ####
logger.info("******** Complex *******")
try:
    complex = list(Complex.get_all(physical_location_id=COMPLEX_ID))[0]
    logger.info("Complex exists")
except IndexError:
    logger.info("Complex does not exists")
    complex = Complex.create(physical_location_id=COMPLEX_ID,
                             name=COMPLEX_ID,
                             physical_location_type="office",
                             street1="DummyStreet 1",
                             city="DummyCity",
                             postal_code="00-000",
                             country="DummyCountry",
                             region="DummyRegion")
    logger.info("Complex created")

#### Create cloud region if not exists ####
logger.info("******** Cloud Region *******")
try:
    cloud_region = list(CloudRegion.get_all(cloud_owner=CLOUD_OWNER, cloud_region_id=CLOUD_REGION))[0]
    logger.info("Cloud region exists")
except IndexError:
    logger.info("Cloud region does not exists")
    cloud_region = CloudRegion.create(cloud_owner=CLOUD_OWNER,
                                      cloud_region_id=CLOUD_REGION,
                                      cloud_type="k8s",
                                      owner_defined_type="t1",
                                      cloud_region_version="1.0",
                                      complex_name=complex.physical_location_id,
                                      cloud_zone="CloudZone",
                                      sriov_automation="false",
                                      orchestration_disabled=False,
                                      in_maint=False)
    logger.info("Cloud region created")

logger.info("******** Cloud regiongion <-> Complex *******")
cloud_region.link_to_complex(complex)

logger.info("******** Availability zone *******")
cloud_region.add_availability_zone(availability_zone_name=AVAILABILITY_ZONE_NAME,
                                   availability_zone_hypervisor_type=HYPERVISOR_TYPE)

logger.info("******** Tenant *******")
cloud_region.add_tenant(str(uuid4()), TENANT_NAME)

#### Update or create connectivity info ####
logger.info("******** Connectivity Info *******")
with open(os.path.join(MYPATH, CLUSTER_KUBECONFIG_PATH), 'rb') as kubeconfig_file:
    kubeconfig = kubeconfig_file.read()
try:
    connectivity_info = ConnectivityInfo.get_connectivity_info_by_region_id(cloud_region_id=CLOUD_REGION)
    logger.info("Connectivity Info exists ")
    logger.info("Delete Connectivity Info ")
    connectivity_info.delete()
    connectivity_info = ConnectivityInfo.create(cloud_region_id=CLOUD_REGION,
                                                cloud_owner=CLOUD_OWNER,
                                                kubeconfig=kubeconfig)
    logger.info("Connectivity Info created ")
except:
    logger.info("Connectivity Info does not exists ")
    connectivity_info = ConnectivityInfo.create(cloud_region_id=CLOUD_REGION,
                                                cloud_owner=CLOUD_OWNER,
                                                kubeconfig=kubeconfig)
    logger.info("Connectivity Info created ")

#### Create customer if not exists ####
logger.info("******** Customer *******")
try:
    customer = Customer.get_by_global_customer_id(GLOBAL_CUSTOMER_ID)
    logger.info("Customer exists")
except:
    logger.info("Customer exists")
    customer = Customer.create(GLOBAL_CUSTOMER_ID, GLOBAL_CUSTOMER_ID, "INFRA")
    logger.info("Customer created")

#### Add region to SO db ####
logger.info("******** SO Database *******")
so_db_adapter = SoDBAdapter(cloud_region_id=CLOUD_REGION,
                            complex_id=COMPLEX_ID,
                            onap_kubeconfig_path=ONAP_KUBECONFIG_PATH)
is_region_in_so = so_db_adapter.check_region_in_db()

if not is_region_in_so:
    so_db_adapter.add_region_to_so_db()

