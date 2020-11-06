#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import logging

from config import *
from onapsdk.aai.cloud_infrastructure import (
    CloudRegion,
)
from onapsdk.aai.business import (
    Customer,
    OwningEntity as AaiOwningEntity
)
from onapsdk.msb.k8s import Definition

from onapsdk.so.instantiation import (
    ServiceInstantiation,
    InstantiationParameter, VnfParameters, VfmoduleParameters)
from onapsdk.sdc.service import Service
from onapsdk.vid import LineOfBusiness, OwningEntity, Platform, Project

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
fh = logging.StreamHandler()
fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)

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
        vf_module_label = vf_module.properties["vf_module_label"]
        profile_name = VF_MODULE_LIST[vf_module_label]["k8s-rb-profile-name"]
        try:
            profile = definition.get_profile_by_name(profile_name)
            if profile.namespace != VF_MODULE_LIST[vf_module_label]["k8s-rb-profile-namespace"]:
                profile.delete()
                logger.info("Profile: " + profile_name + " for " + vf_module.name + " deleted")
            else:
                logger.info("No need to delete Profile " + profile_name +
                            " for " + vf_module.name + ". Namespace is fine")
        except ValueError:
            logger.info("Profile: " + profile_name + " for " + vf_module.name + " not found")


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
        InstantiationParameter(name="sdnc_artifact_name", value=SDNC_ARTIFACT_NAME)]

    vfmodules_param = []
    for vfmodule in vfmodules_list:
        params = [
            InstantiationParameter(name="k8s-rb-profile-name", value=vfmodules_list[vfmodule]["k8s-rb-profile-name"]),
            InstantiationParameter(name="k8s-rb-profile-namespace", value=vfmodules_list[vfmodule]["k8s-rb-profile-namespace"]),
            InstantiationParameter(name="sdnc_model_name", value=SDNC_MODEL_NAME),
            InstantiationParameter(name="sdnc_model_version", value=SDNC_MODEL_VERSION),
            InstantiationParameter(name="vf_module_label", value=vfmodules_list[vfmodule]["name"])]

        vfmodules_param.append(VfmoduleParameters(vfmodules_list[vfmodule]["name"], params))

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

