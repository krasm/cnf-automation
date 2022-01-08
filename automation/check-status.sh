#!/bin/sh

VERBOSE=-v

usage() {
    echo $0 instantitation_request_id service_id vnf_id
    exit 0
}

SELF_LINK=$1
echo "querying $SELF_LINK"

curl -v -x "socks5h://127.0.0.1:1082" \
    -H'Authorization: Basic YnBlbDpwYXNzd29yZDEk' \
    -H'Content-type: application/json' \
    $SELF_LINK
