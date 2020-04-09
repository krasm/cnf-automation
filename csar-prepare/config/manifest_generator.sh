#!/bin/bash
service_name="$1"
service_description="$2"
CNFs="$3"
base_chart="$4"
data_content=""

for CNF in $CNFs
do
  env_name="${CNF}.env"
  yaml_name="${CNF}.yaml"
  base="false"

  if [ $CNF = $base_chart ]
  then
    base="true"
  fi

  output=$(jo -p file=$yaml_name type=HEAT -B isBase=$base data[]=$(jo file=$env_name type=HEAT_ENV))

  if [ -z "$data_content" ]
  then
    data_content="$output"
  else
  data_content="$data_content,$output"
  fi

  tgz_name="${CNF}_cloudtech_k8s_charts.tgz"
  output=$(jo -p file=$tgz_name type=CLOUD_TECHNOLOGY_SPECIFIC_ARTIFACTS)
  data_content="$data_content,$output"
done

jo -p name="$service_name" description="$service_description" data="[$data_content]"
