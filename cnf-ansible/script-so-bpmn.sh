#!/bin/bash
name=$(kubectl -n onap get configmap | grep so-bpmn-infra-app-configmap)
kubectl -n onap get configmap $name -o json > tmp/configmap.json

search_string="http://so-openstack-adapter.onap:8087/services/rest/v1/vnfs"
new_string="http://so-openstack-adapter.onap:8087/services/rest/v2/vnfs"
sed -i "s|${search_string}|${new_string}|g" tmp/configmap.json

kubectl -n onap apply -f tmp/configmap.json
kubectl -n onap delete pod -l app=so-bpmn-infra
