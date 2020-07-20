# Prepare CSAR for CNF orchestrated with ONAP
In order to prepare CSAR archive that will be consumed by ONAP during onboarding phase you need to perform three steps.
  - put all charts that CNF consists of into **charts/** directory
  - edit **config/config.yml** file and provide service name, service description and base chart name
  - run csar-prepare.yml playbook

  ``` $ ansible-playbook csar-prepare.yml```

Once the script is CSAR package named **{{service_name}}_CNF.zip** could be found in the root directory. Moreover csar/, helm/ and heat/ directories are created.
