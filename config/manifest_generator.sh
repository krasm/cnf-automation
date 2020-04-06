#!/bin/bash
service_name="$1"
service_description="$2"
service_package_name="$3"
CNFs="$4"

data_content=$(jo -p file=$service_package_name.zip type=CONTROLLER_BLUEPRINT_ARCHIVE)

for CNF in $CNFs
do
  env_name="$CNF.env"
  yaml_name="$CNF.yaml"
  output=$(jo -p file=$yaml_name type=HEAT -B isBase=true data[]=$(jo file=$env_name type=HEAT_ENV))
  data_content="$data_content,$output"
  tgz_name="${CNF}_cloudtech_k8s_charts.tgz"
  output=$(jo -p file=$tgz_name type=CLOUD_TECHNOLOGY_SPECIFIC_ARTIFACTS)
  data_content="$data_content,$output"
done

jo -p name="$service_name" description="$service_description" data="[$data_content]"
