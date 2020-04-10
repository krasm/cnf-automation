#!/bin/bash
CNFs="$1"
base="$2"

for CNF in $CNFs
do
  cp dummy/dummy.yaml ../heat/${CNF}.yaml

  if [ $CNF != $base ]
  then
    yq d -i ../heat/${CNF}.yaml  resources.dummy_base
  fi
done

