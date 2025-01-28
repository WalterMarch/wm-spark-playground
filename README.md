# Spark Playground

This Spark Playground has the following installed:

* Apache Spark
* MySQL Server
* Python
* PySpark
* R
* Scala

I enjoy working with data and Extract-Transform-Load (ETL) pipelines and am looking forward to playing around with Spark and friends.

## configit.sh

This repository's *devcontainer.json* uses a `postCreateCommand` to run `configit.sh`.

This script uses information particular to the user of the repository.

```shell
#!/bin/bash

git config --global user.email "yourEmail@mail.com"
git config --global user.name "yourGitUserName"
git config --global push.autoSetupRemote true
git config --global push.default current
git config --global init.defaultBranch main
git config --global --add safe.directory $1
```
