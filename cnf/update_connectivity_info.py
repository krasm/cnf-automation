import logging
import os

from cnf.config import *
from onapsdk.msb.k8s import ConnectivityInfo

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
fh = logging.StreamHandler()
fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)

MYPATH = os.path.dirname(os.path.realpath(__file__))

logger.info("******** Connectivity Info *******")
with open(os.path.join(MYPATH, CLUSTER_KUBECONFIG_PATH), 'rb') as kubeconfig_file:
    kubeconfig = kubeconfig_file.read()
try:
    connectivity_info = ConnectivityInfo.get_connectivity_info_by_region_id(cloud_region_id=CLOUD_REGION)
    logger.info("Connectivity Info exists ")
    logger.info("Delete Connectivity Info exists ")
    connectivity_info.delete()
    connectivity_info = ConnectivityInfo.create(cloud_region_id=CLOUD_REGION,
                                                cloud_owner=CLOUD_OWNER,
                                                kubeconfig=kubeconfig)
except:
    logger.info("Connectivity Info does not exists ")
    connectivity_info = ConnectivityInfo.create(cloud_region_id=CLOUD_REGION,
                                                cloud_owner=CLOUD_OWNER,
                                                kubeconfig=kubeconfig)
    logger.info("Connectivity Info created ")

