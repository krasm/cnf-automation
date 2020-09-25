#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""E2E Instantiation of vFW"""

import logging
import string
import sys
import time
from uuid import uuid4
# from onapsdk.aai.aai_element import AaiElement
from onapsdk.aai.cloud_infrastructure import (
    CloudRegion,
    Complex,
    Tenant
)
# from onapsdk.aai.service_design_and_creation import (
#    Service as AaiService
# )
from onapsdk.aai.business import (
    ServiceInstance,
    VnfInstance,
    VfModuleInstance,
    ServiceSubscription,
    Customer,
    OwningEntity as AaiOwningEntity
)
from onapsdk.msb.k8s import Definition
from onapsdk.sdc.properties import Property
from onapsdk.so.instantiation import (
    ServiceInstantiation,
    VnfInstantiation,
    VnfParameter,
    InstantiationParameter, VnfParameters, VfmoduleParameters)
# from onapsdk.sdc import SDC
from onapsdk.sdc.vendor import Vendor
from onapsdk.sdc.vsp import Vsp
from onapsdk.sdc.vf import Vf
from onapsdk.sdc.service import Service, ServiceInstantiationType
# import onapsdk.constants as const
import os
from onapsdk.vid import LineOfBusiness, OwningEntity, Platform, Project

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
fh = logging.StreamHandler()
fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)

# Create required A&AI resources
VENDOR = sys.argv[1]
VSPFILE = "../../csar-prepare/" + sys.argv[6] + "_CNF.zip"
VSPNAME = "VSP_" + sys.argv[6]
VFNAME = "VF_" + sys.argv[6]
SERVICENAME = "SERVICE_" + sys.argv[6]

GLOBAL_CUSTOMER_ID = sys.argv[2]

CLOUD_OWNER = sys.argv[3]
CLOUD_REGION = sys.argv[4]
TENANT_NAME = sys.argv[5]

######## DEFAULT VALUES ########
OWNING_ENTITY = "OE-Demonstration"
PROJECT = "Project-Demonstration"
PLATFORM = "test"
LINE_OF_BUSINESS = "LOB-Demonstration"

SERVICE_INSTANCE_NAME = "INSTANCE_" + sys.argv[6] + "6"

###### MACRO INSTANTIATION PARAMETERS #####
SDNC_MODEL_NAME = sys.argv[7]
SDNC_MODEL_VERSION = sys.argv[8]
K8S_RB_PROFILE_NAME = sys.argv[9]
K8S_RB_PROFILE_NAMESPACE = sys.argv[10]
VF_MODULE_LIST = sys.argv[11]

logger.info("*******************************")
logger.info("******** SERVICE DESIGN *******")
logger.info("*******************************")

logger.info("******** Onboard Vendor *******")
vendor = Vendor(name=VENDOR)
vendor.onboard()

logger.info("******** Onboard VSP *******")
mypath = os.path.dirname(os.path.realpath(__file__))
myvspfile = os.path.join(mypath, VSPFILE)
vsp = Vsp(name=VSPNAME, vendor=vendor, package=open(myvspfile, 'rb'))
vsp.onboard()

logger.info("******** Onboard VF *******")
vf = Vf(name=VFNAME, properties=[
    Property(name="sdnc_model_name", property_type="string", value=SDNC_MODEL_NAME),
    Property(name="sdnc_model_version", property_type="string", value=SDNC_MODEL_VERSION),
    Property(name="sdnc_artifact_name", property_type="string", value="vnf")
    ]
        )
vf.vsp = vsp
vf.onboard()

logger.info("******** Onboard Service *******")
svc = Service(name=SERVICENAME, resources=[vf], instantiation_type=ServiceInstantiationType.MACRO)
svc.onboard()

logger.info("******** Check Service Distribution *******")
distribution_completed = False
nb_try = 0
nb_try_max = 10
while distribution_completed is False and nb_try < nb_try_max:
    distribution_completed = svc.distributed
    if distribution_completed is True:
        logger.info("Service Distribution for %s is sucessfully finished", svc.name)
        break
    logger.info("Service Distribution for %s ongoing, Wait for 60 s", svc.name)
    time.sleep(60)
    nb_try += 1

if distribution_completed is False:
    logger.error("Service Distribution for %s failed !!", svc.name)
    exit(1)

logger.info("*******************************")
logger.info("**** SERVICE INSTANTIATION ****")
logger.info("*******************************")

logger.info("******** Create Customer *******")
customer = None
for found_customer in list(Customer.get_all()):
    logger.debug("Customer %s found", found_customer.subscriber_name)
    if found_customer.subscriber_name == GLOBAL_CUSTOMER_ID:
        logger.info("Customer %s found", found_customer.subscriber_name)
        customer = found_customer
        break
if not customer:
    customer = Customer.create(GLOBAL_CUSTOMER_ID, GLOBAL_CUSTOMER_ID, "INFRA")

logger.info("******** Find Service in SDC *******")
service = None
services = Service.get_all()
for found_service in services:
    logger.debug("Service %s is found, distribution %s", found_service.name, found_service.distribution_status)
    if found_service.name == SERVICENAME:
        logger.info("Found Service %s in SDC", found_service.name)
        service = found_service
        break

if not service:
    logger.error("Service %s not found in SDC", SERVICENAME)
    exit(1)

logger.info("******** Check Service Subscription *******")
service_subscription = None
for service_sub in customer.service_subscriptions:
    logger.debug("Service subscription %s is found", service_sub.service_type)
    if service_sub.service_type == SERVICENAME:
        logger.info("Service %s subscribed", SERVICENAME)
        service_subscription = service_sub
        break

if not service_subscription:
    logger.info("******** Subscribe Service *******")
    customer.subscribe_service(service)

logger.info("******** Get Tenant *******")
cloud_region = CloudRegion(cloud_owner=CLOUD_OWNER, cloud_region_id=CLOUD_REGION,
                           orchestration_disabled=True, in_maint=False)
tenant = None
for found_tenant in cloud_region.tenants:
    logger.debug("Tenant %s found in %s_%s", found_tenant.name, cloud_region.cloud_owner, cloud_region.cloud_region_id)
    if found_tenant.name == TENANT_NAME:
        logger.info("Found my Tenant %s", found_tenant.name)
        tenant = found_tenant
        break

if not tenant:
    logger.error("tenant %s not found", TENANT_NAME)
    exit(1)

logger.info("******** Connect Service to Tenant *******")
service_subscription = None
for service_sub in customer.service_subscriptions:
    logger.debug("Service subscription %s is found", service_sub.service_type)
    if service_sub.service_type == SERVICENAME:
        logger.info("Service %s subscribed", SERVICENAME)
        service_subscription = service_sub
        break

if not service_subscription:
    logger.error("Service subscription %s is not found", SERVICENAME)
    exit(1)

service_subscription.link_to_cloud_region_and_tenant(cloud_region, tenant)

logger.info("******** Add Business Objects (OE, P, Pl, LoB) in VID *******")
vid_owning_entity = OwningEntity.create(OWNING_ENTITY)
vid_project = Project.create(PROJECT)
vid_platform = Platform.create(PLATFORM)
vid_line_of_business = LineOfBusiness.create(LINE_OF_BUSINESS)

logger.info("******** Add Owning Entity in AAI *******")
owning_entity = None
for oe in AaiOwningEntity.get_all():
    if oe.name == vid_owning_entity.name:
        owning_entity = oe
        break
if not owning_entity:
    logger.info("******** Owning Entity not existing: create *******")
    owning_entity = AaiOwningEntity.create(vid_owning_entity.name, str(uuid4()))

logger.info("******** Delete old profiles ********")
for vnf in service.vnfs:
    for vf_module in vnf.vf_modules:
        definition = Definition.get_definition_by_name_version(vf_module.metadata["vfModuleModelInvariantUUID"],
                                                                   vf_module.metadata["vfModuleModelUUID"])
        try:
            profile = definition.get_profile_by_name("vfw-cnf-cds-base-profile")
            profile.delete()
        except ValueError:
            logger.info("Profile: vfw-cnf-cds-base-profile for " + vf_module.name + "not found")

logger.info("******** Instantiate Service *******")
service_instance = None
service_instantiation = None
for se in service_subscription.service_instances:
    if se.instance_name == SERVICE_INSTANCE_NAME:
        service_instance = se
        break
if not service_instance:
    logger.info("******** Service Instance not existing: Instantiate *******")
    # Instantiate service
    vfmodules_list = VF_MODULE_LIST

    vnf_param = [
        InstantiationParameter(name="sdnc_model_name", value=SDNC_MODEL_NAME),
        InstantiationParameter(name="sdnc_model_version", value=SDNC_MODEL_VERSION),
        InstantiationParameter(name="sdnc_artifact_name", value="vnf")]

    vfmodules_param = []
    for vfmodule in vfmodules_list:
        params = [
            InstantiationParameter(name="k8s-rb-profile-name", value=K8S_RB_PROFILE_NAME),
            InstantiationParameter(name="k8s-rb-profile-namespace", value=K8S_RB_PROFILE_NAMESPACE),
            InstantiationParameter(name="sdnc_model_name", value=SDNC_MODEL_NAME),
            InstantiationParameter(name="sdnc_model_version", value=SDNC_MODEL_VERSION),
            InstantiationParameter(name="vf_module_label", value=vfmodule)]
        vfmodules_param.append(VfmoduleParameters(vfmodule, params))

    vnf_params = VnfParameters(name=VFNAME, vnf_parameters=vnf_param, vfmodule_parameters=vfmodules_param)

    service_instantiation = ServiceInstantiation.instantiate_macro(
        service,
        cloud_region,
        tenant,
        customer,
        owning_entity,
        vid_project,
        vid_line_of_business,
        vid_platform,
        service_instance_name=SERVICE_INSTANCE_NAME,
        vnf_parameters=[vnf_params]
    )
