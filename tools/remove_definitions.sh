#!/bin/bash

definitions=$(curl -L -X GET 'http://10.254.184.22:30280/api/multicloud-k8s/v1/v1/rb/definition')

for row in $(echo "$definitions" | jq -c '.[]')
do
  rb_name=$(echo ${row} | jq -r '."rb-name"')
  rb_version=$(echo ${row} | jq -r '."rb-version"')

  curl -L -X DELETE http://10.254.184.22:30280/api/multicloud-k8s/v1/v1/rb/definition/$rb_name/$rb_version
done
