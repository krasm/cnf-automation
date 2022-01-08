#!/usr/bin/env python3

import logging
import requests
import json
import uuid

from config import Config

#FIXME remove from global scope
logger = logging.getLogger("")
logger.setLevel(logging.INFO)
fh = logging.StreamHandler()
fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)

proxies = {
    'http': 'socks5h://127.0.0.1:1082',
    'https': 'socks5h://127.0.0.1:1082'
}
session = requests.Session()
session.proxies.update(proxies)
session.verify = False

def get_customer_subscriptions(customer):
    logger.info('retireve customer subscriptions for ' + customer)
    URL = 'https://aai.api.sparky.simpledemo.onap.org:30233'
    PATH = f'aai/v20/business/customers/customer/{customer}/service-subscriptions'
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'x-fromappid': 'AAI',
               'x-transactionid': f'{uuid.uuid4()}',
               'authorization': 'Basic QUFJOkFBSQ=='}

    r = session.get(f'{URL}/{PATH}', headers=headers)
    r.raise_for_status()

    result = map(lambda x: x['service-type'], r.json()['service-subscription'])
    return list(result)

def get_service_metadata(customer, subscriptions):
    URL = 'https://aai.api.sparky.simpledemo.onap.org:30233'
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'x-fromappid': 'AAI',
               'x-transactionid': f'{uuid.uuid4()}',
               'authorization': 'Basic QUFJOkFBSQ=='}

    result = []
    for sub in subscriptions:
        PATH = f'/aai/v20/business/customers/customer/{customer}/service-subscriptions/service-subscription/{sub}/service-instances'
        logger.info(f'retrieving service metadata for subscription: {sub} and customer: {customer}')

        r = session.get(f'{URL}{PATH}', headers=headers)
        r.raise_for_status()

        t = r.json()['service-instance']
        if len(t) != 1:
            raise Exception('multi vnf services are not supported')
        t = t[0]
        for rel in t['relationship-list']['relationship']:
            if rel['related-to'] == 'generic-vnf' and rel['relationship-label'] == 'org.onap.relationships.inventory.ComposedOf':
                path = rel['related-link']
                r = session.get(f'{URL}{path}', headers=headers)
                r.raise_for_status()

                r = r.json()
                result.append({'instanceId': r['vnf-id'],
                               'instanceName': r['vnf-name'],
                               'modelInfo': {
                                   'modelType': 'vnf',
                                   'modelInvariantId': r['model-invariant-id'],
                                   'modelVersionId': r['model-version-id'],
                                   'modelCustomizationId': r['model-customization-id'],
                                   'modelVersion': '1.0',
                                   'modelName': 'APACHE'
                               }
                               })

    return result

def get_service(name):
    logger.info('retrieve service ' + name)
    CATALOG_DB_URL = 'https://sdc.api.fe.simpledemo.onap.org:30204/sdc/v1/catalog/services'
    headers = {'Accept': 'application/json',
               'Authorization': 'Basic dmlkOktwOGJKNFNYc3pNMFdYbGhhazNlSGxjc2UyZ0F3ODR2YW9HR21KdlV5MlU=',
               'X-ECOMP-InstanceID': 'VID'}

    r = session.get(CATALOG_DB_URL, headers=headers)
    r.raise_for_status()

    for i in r.json():
        if i['name'] == name:
            return i

    raise Exception('No service ' + name + ' was found')


def get_service_model(service_uuid):
    CATALOG_DB_URL = "http://aai.api.simpledemo.onap.org:32090/ecomp/mso/catalog/v2/serviceVnfs?serviceModelUuid="
    headers = {'Accept': 'application/json',
               'Authorization': 'Basic YnBlbDpwYXNzd29yZDEk'}

    r = session.get(CATALOG_DB_URL + service_uuid, headers=headers)
    if r.status_code != 200:
        raise Exception('Failed to query catalog')

    return r.json()


def main():
    logger.info('retrieving service metadata')
    srv = get_service(Config.SERVICENAME)
    model = get_service_model(srv['uuid'])

    subs = get_customer_subscriptions(Config.GLOBAL_CUSTOMER_ID)
    instances = get_service_metadata(Config.GLOBAL_CUSTOMER_ID, subs)

    if len(model['serviceVnfs']) != 1:
        raise Exception('Only single VNF services are currently supported')
    modelInfo = model['serviceVnfs'][0]['modelInfo']

    print("******* SERVICE ******")
    print(modelInfo)
    print("****** SERVICE ******")

    logger.info('building request')
    t = {'instanceId': '1695bef1-1a83-4419-9e7e-9bb250b73f6b',
         'instanceName': 'INSTANCE_apache_k8s_demo_CNF',
         'modelInfo': {
                'modelName': modelInfo['modelName'],
                'modelType': "vnf",
                'modelInvariantId': modelInfo['modelInvariantUuid'],
                'modelVersionId': modelInfo['modelCustomizationUuid'],
                'modelVersion': modelInfo['modelVersion'],
                'modelCustomizationName': modelInfo['modelInstanceName']
         }
         }
    request = {
        'requestDetails': {
            'modelInfo': {
                'modelName': modelInfo['modelName'],
                'modelType': "vnf",
                'modelInvariantId': modelInfo['modelInvariantUuid'],
                'modelNameVersionId': modelInfo['modelCustomizationUuid'],
                'modelVersion': modelInfo['modelVersion'],
                'modelCustomizationName': modelInfo['modelInstanceName']
            },
            'cloudConfiguration': {
                'lcpCloudRegionId': Config.K8S_REGION,
                'tenantId': '9680dc64-a934-4ea2-930d-72edf6c377d3'
            },
            'requestInfo': {
                'instanceName': Config.SERVICE_INSTANCE_NAME,
                'source': 'testmsk',
                'suppressRollback': False,
                'requestorId': 'abcdefgh'
            },
            'relatedInstanceList': [
                {'relatedInstance': t}
            ]
        }
    }
    logger.info(request)

    logger.info('requesting healthcheck')
    r = session.post('http://so.api.simpledemo.onap.org:30277/onap/so/infra/serviceInstantiation/v7/serviceInstances/1695bef1-1a83-4419-9e7e-9bb250b73f6b/vnfs/3c2644bf-3ad6-42f2-8c96-454b2e0df371/healthcheck',
#    r = session.post('http://so.api.simpledemo.onap.org:30277/onap/so/infra/serviceInstantiation/v7/serviceInstances/',
                 headers={'Authorization': 'Basic YnBlbDpwYXNzd29yZDEk',
                          'Content-type': 'application/json',
                          'Accept': 'application/json'},
                 data=json.dumps(request))
    print(r.text)
    r.raise_for_status()

if __name__ == '__main__':
    main()

