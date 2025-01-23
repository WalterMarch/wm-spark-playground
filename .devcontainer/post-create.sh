#!/bin/bash

.devcontainer/configit.sh  $1

mkdir ~/minio
minio server ~/minio --console-address :9001