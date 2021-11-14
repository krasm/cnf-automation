Demo directory structure:

/templates/           #Base directory containing vFW resources
    |- /base_native   #Directory containing base payload of VSP package in Helm VSP, doesn't need further proceeding
    |- /helm          #Directory containing helm charts that need to be packaged and attached to VSP package
    \- /cba           #Directory containing CBA content to be included to csar package.
/examples/            #Directory with context-specific overrides over general resources
/automation/          #Directory with automation scripts. For more details read README file inside.

Note: Makefile script generates VSP package in native Helm VSP format where helm packages are standalone.
