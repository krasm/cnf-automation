#!/bin/bash
CNFs="$1"

for CNF in $CNFs
do
  cp dummy/dummy.env ../heat/${CNF}.env
  vnf_id=$(uuidgen)
  vf_module_id=$(uuidgen)
  yq w -i ../heat/${CNF}.env  parameters.vnf_id $vnf_id
  yq w -i ../heat/${CNF}.env  parameters.vnf_name ${CNF}
  yq w -i ../heat/${CNF}.env  parameters.vf_module_id $vf_module_id
done
