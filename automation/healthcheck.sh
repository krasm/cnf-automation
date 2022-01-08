#!/bin/sh

VERBOSE=-v

usage() {
    echo $0 instantitation_request_id service_id vnf_id
    exit 0
}

#kubectl expose service so-catalog-db-adapter --type=NodePort --name=x-so-catalog-db-adapter
#SERVICE_INSTANCE_ID=1695bef1-1a83-4419-9e7e-9bb250b73f6b

INSTANTIATION_REQUEST_ID=$1
SERVICE_INSTANCE_ID=$2
VNF_INSTANCE_ID=$3


echo "executing with instatntiation request id $INSTANTIATION_REQUEST_ID, service_id $SERVICE_ID and vnf_id $VNF_ID"

REQUEST_DATA='{
    "requestDetails": {
        "requestInfo": {
            "suppressRollback": false,
            "productFamilyId":"apache_k8s_demo_CNF",
            "requestorId": "mskdemo",
            "instanceName": "INSTANCE_apache_k8s_demo_CNF",
            "source": "VID"
        },
        "modelInfo": {
            "modelType": "service",
			"modelInvariantId": "089de6e6-79b4-4e0f-84ef-85263c0cf781",
			"modelVersionId": "bd756298-4882-4275-9d19-106dd925ca82",
			"modelName": "apache_k8s_demo_CNF",
            "modelVersion": "1.0"
        },
        "cloudConfiguration": {
            "tenantId": "9680dc64-a934-4ea2-930d-72edf6c377d3",
            "cloudOwner": "K8sCloudOwner",
            "lcpCloudRegionId": "cnf-region"
        },
        
        "subscriberInfo": {
            "globalSubscriberId": "customer_cnf"
        },
        "requestParameters": {
            "subscriptionServiceType": "apache_k8s_demo_CNF",
            "userParams": [
                {
                    "Homing_Solution": "none"
                },
                
                {
                    "service": {
                        "instanceParams": [],
                        "instanceName": "INSTANCE_apache_k8s_demo_CNF",
                        "resources": {
                            
                            
                            "vnfs": [
                                
                                {
                                    "modelInfo": {
                                        "modelName": "VF_apache_k8s_demo_CNF",
                                        "modelVersionId": "61b56deb-4d4d-4445-ba2c-1105d43d8fb7",
                                        "modelInvariantUuid": "e04ae80a-6ae3-48e5-88a2-93cf07d27e3d",
                                        "modelVersion": "1.0",
                                        "modelCustomizationId": "d74fbd32-19e1-43ec-9b9b-511b25abbf91",
                                        "modelInstanceName": "VF_apache_k8s_demo_CNF"
                                    },
                                    "cloudConfiguration": {
                                        "tenantId": "9680dc64-a934-4ea2-930d-72edf6c377d3",
                                        "cloudOwner": "K8sCloudOwner",
                                        "lcpCloudRegionId": "cnf-region"
                                    },
                                    "platform": {
                                        "platformName": "test"
                                    },
                                    "lineOfBusiness": {
                                        "lineOfBusinessName": "LOB-Demonstration"
                                    },
                                    "productFamilyId": "1234",
                                    "instanceName": "VF_apache_k8s_demo_CNF",
                                    "instanceParams": [
                                        {
                                            
                                            
                                            
                                            "sdnc_model_name": "APACHE",
                                            
                                            "sdnc_model_version": "1.0.0",
                                            
                                            "sdnc_artifact_name": "vnf",
                                            
                                            "k8s-rb-profile-namespace": "test-cnf",
                                            
                                            "k8s-rb-profile-k8s-version": "1.18.9"
                                            
                                            
                                            
                                        }
                                    ],
                                    "vfModules": [
                                        
                                        {
                                            "modelInfo": {
                                                "modelName": "VfApacheK8sDemoCnf..helm_apache..module-1",
                                                "modelVersionId": "ad69cc0e-e30f-44ce-9fc2-dde0e7657722",
                                                "modelInvariantUuid": "cdfaf71e-5a28-4341-90b1-c2e59b9bf2ed",
                                                "modelVersion": "1",
                                                "modelCustomizationId": "55d9832b-70b4-40e3-be61-70c624091522"
                                            },
                                            "instanceName": "INSTANCE_apache_k8s_demo_CNF_vf_apache_k8s_demo_cnf0..VfApacheK8sDemoCnf..helm_apache..module-1",
                                            "instanceParams": [
                                                {
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    "sdnc_model_name": "APACHE",
                                                    
                                                    "sdnc_model_version": "1.0.0",
                                                    
                                                    "vf_module_label": "helm_apache",
                                                    
                                                    "k8s-rb-profile-name": "node-port-profile",
                                                    
                                                    "k8s-rb-profile-source": "node-port-profile",
                                                    
                                                    "k8s-rb-instance-release-name": "rel-1-apache",
                                                    
                                                    "k8s-rb-profile-namespace": "test-cnf",
                                                    
                                                    "k8s-rb-config-template-name": "replica-count-template",
                                                    
                                                    "k8s-rb-config-template-source": "deployment-config",
                                                    
                                                    "k8s-rb-config-name": "replica-count-change",
                                                    
                                                    "k8s-rb-config-value-source": "custom-values"
                                                    
                                                    
                                                    
                                                    
                                                    
                                                }
                                            ]
                                        },
                                        
                                        {
                                            "modelInfo": {
                                                "modelName": "VfApacheK8sDemoCnf..base_template_dummy_ignore..module-0",
                                                "modelVersionId": "0eeebb44-fe5d-40d1-b630-5dd6aa6a52c5",
                                                "modelInvariantUuid": "621c5d68-bf64-4976-be25-89be4275272c",
                                                "modelVersion": "1",
                                                "modelCustomizationId": "13c3a2ca-426e-49a2-a348-70e0250c0d21"
                                            },
                                            "instanceName": "INSTANCE_apache_k8s_demo_CNF_vf_apache_k8s_demo_cnf0..VfApacheK8sDemoCnf..base_template_dummy_ignore..module-0",
                                            "instanceParams": [
                                                {
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    
                                                }
                                            ]
                                        }
                                        
                                    ]
                                }
                                
                            ]
                            
                        },
                        "modelInfo": {
                            "modelVersion": "1.0",
                            "modelVersionId": "bd756298-4882-4275-9d19-106dd925ca82",
                            "modelInvariantId": "089de6e6-79b4-4e0f-84ef-85263c0cf781",
                            "modelName": "apache_k8s_demo_CNF",
                            "modelType": "service"
                        }
                    }
                }
            ],
            "aLaCarte": false
        },
        "project": {
            "projectName": "Project-Demonstration"
        },
        "owningEntity": {
            "owningEntityId": "d66ff93a-38d9-4dbf-9f58-15ab4e4938d7",
            "owningEntityName": "OE-Demonstration"
        }
    }
}'


#echo "retrieving services"
#FILENAME=$(mktemp)
#curl $VERBOSE -k -x "socks5h://127.0.0.1:1082" -X GET \
#    -H "Accept: application/json" \
#    -H "Authorization: Basic dmlkOktwOGJKNFNYc3pNMFdYbGhhazNlSGxjc2UyZ0F3ODR2YW9HR21KdlV5MlU=" \
#    -H "X-ECOMP-InstanceID: VID" \
#    https://sdc.api.fe.simpledemo.onap.org:30204/sdc/v1/catalog/services 1>$FILENAME
#
#SERVICE_UUID=$(cat $FILENAME | jq '.[0].uuid')
#SERVICE_INVARIANT_UUID=$(cat $FILENAME | jq '.[0].invariantUUID')
#SERVICE_NAME=$(cat $FILENAME | jq '.[0].name')
#SERVICE_VERSION=$(cat $FILENAME | jq '.[0].version')
#SERVICE_TOSCA_MODEL_URL=$(cat $FILENAME | jq '.[0].toscaModelURL')
#    
#echo "service uuid: $SERVICE_UUID"
#echo "service invariant uuid: $SERVICE_INVARIANT_UUID"
#echo "service name: $SERVICE_NAME"
#echo "service version: $SERVICE_VERSION"
#echo "service tosca model url: $SERVICE_TOSCA_MODEL_URL"
#
#curl $VERBOSE -x "socks5h://127.0.0.1:1082" -X GET \
#    -H "Accept: application/json" \
#    -H "Authorization: Basic YnBlbDpwYXNzd29yZDEk" \
#    http://aai.api.simpledemo.onap.org:$CATALOG_DB_PORT/ecomp/mso/catalog/v2/serviceVnfs?serviceModelUuid=bd756298-4882-4275-9d19-106dd925ca82  #$SERVICE_UUID
#
#

echo "requesting instantiation status to obtain request context"
REQUEST_DETAILS=$(mktemp)
echo "{\"requestDetails\":" > $REQUEST_DETAILS

curl -v -x "socks5h://127.0.0.1:1082"  \
    -H'Authorization: Basic YnBlbDpwYXNzd29yZDEk' \
    -H'Content-type: application/json' \
    "http://so.api.simpledemo.onap.org:30277/onap/so/infra/orchestrationRequests/v7/$INSTANTIATION_REQUEST_ID" | \
    jq .request.requestDetails | tee -a $REQUEST_DETAILS

echo "}" >> $REQUEST_DETAILS

curl -v -x "socks5h://127.0.0.1:1082" -X POST \
    -H'Authorization: Basic YnBlbDpwYXNzd29yZDEk' \
    -H'Content-type: application/json' \
    -d "@$REQUEST_DETAILS" \
    http://so.api.simpledemo.onap.org:30277/onap/so/infra/serviceInstantiation/v7/serviceInstances/$SERVICE_INSTANCE_ID/vnfs/$VNF_INSTANCE_ID/healthcheck 

