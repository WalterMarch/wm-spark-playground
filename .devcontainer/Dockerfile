#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
FROM --platform=$BUILDPLATFORM eclipse-temurin:17-jammy

# useradd from my work

ARG spark_uid=185
ARG USERNAME=spark
ARG USER_UID=$spark_uid
ARG USER_GID=$USER_UID
ARG USER_SHELL=/bin/sh
ARG USER_SHELL=/bin/bash

# Create the user
RUN groupadd --system --gid $USER_GID $USERNAME \
    && useradd --system --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && usermod -s $USER_SHELL $USERNAME

# https://github.com/apache/spark-docker/blob/master/3.5.4/scala2.12-java17-ubuntu/Dockerfile

RUN set -ex; \
    apt-get update; \
    apt-get install -y gnupg2 wget bash tini libc6 libpam-modules krb5-user libnss3 procps net-tools gosu libnss-wrapper; \
    mkdir -p /opt/spark; \
    mkdir /opt/spark/python; \
    mkdir -p /opt/spark/examples; \
    mkdir -p /opt/spark/work-dir; \
    chmod g+w /opt/spark/work-dir; \
    touch /opt/spark/RELEASE; \
    chown -R $USERNAME:$USERNAME /opt/spark; \
    echo "auth required pam_wheel.so use_uid" >> /etc/pam.d/su; \
    rm -rf /var/lib/apt/lists/*

# Install Apache Spark
# https://downloads.apache.org/spark/KEYS
ENV SPARK_TGZ_URL=https://archive.apache.org/dist/spark/spark-3.5.4/spark-3.5.4-bin-hadoop3.tgz \
    SPARK_TGZ_ASC_URL=https://archive.apache.org/dist/spark/spark-3.5.4/spark-3.5.4-bin-hadoop3.tgz.asc \
    GPG_KEY=19F745C40A0E550420BB2C522541488DA93FE4B4

RUN set -ex; \
    export SPARK_TMP="$(mktemp -d)"; \
    cd $SPARK_TMP; \
    wget -nv -O spark.tgz "$SPARK_TGZ_URL"; \
    wget -nv -O spark.tgz.asc "$SPARK_TGZ_ASC_URL"; \
    export GNUPGHOME="$(mktemp -d)"; \
    gpg --batch --keyserver hkps://keys.openpgp.org --recv-key "$GPG_KEY" || \
    gpg --batch --keyserver hkps://keyserver.ubuntu.com --recv-keys "$GPG_KEY"; \
    gpg --batch --verify spark.tgz.asc spark.tgz; \
    gpgconf --kill all; \
    rm -rf "$GNUPGHOME" spark.tgz.asc; \
    \
    tar -xf spark.tgz --strip-components=1; \
    chown -R $USERNAME:$USERNAME .; \
    mv jars /opt/spark/; \
    mv RELEASE /opt/spark/; \
    mv bin /opt/spark/; \
    mv sbin /opt/spark/; \
    mv kubernetes/dockerfiles/spark/decom.sh /opt/; \
    mv examples /opt/spark/; \
    ln -s "$(basename /opt/spark/examples/jars/spark-examples_*.jar)" /opt/spark/examples/jars/spark-examples.jar; \
    mv kubernetes/tests /opt/spark/; \
    mv data /opt/spark/; \
    mv python/pyspark /opt/spark/python/pyspark/; \
    mv python/lib /opt/spark/python/lib/; \
    mv R /opt/spark/; \
    chmod a+x /opt/decom.sh; \
    cd ..; \
    rm -rf "$SPARK_TMP";

COPY entrypoint.sh /opt/

ENV SPARK_HOME /opt/spark

WORKDIR /opt/spark/work-dir

# https://github.com/apache/spark-docker/blob/master/3.5.4/scala2.12-java17-python3-r-ubuntu/Dockerfile

RUN set -ex; \
    apt-get update; \
    apt-get install -y python3 python3-pip; \
    apt-get install -y r-base r-base-dev; \
    apt-get install -y git tree; \
    rm -rf /var/lib/apt/lists/*; \
    ln -fs /usr/bin/python3 /usr/bin/python

ENV R_HOME /usr/lib/R

RUN echo "export SPARK_HOME=/opt/spark" >> ~/.bashrc; \
 echo "export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin" >> ~/.bashrc; \
 echo "export PYSPARK_PYTHON=/usr/bin/python3" >> ~/.bashrc

# MySQL
RUN apt-get update; apt-get install -y mysql-server

# minIO
RUN wget https://dl.min.io/server/minio/release/linux-amd64/archive/minio_20241218131544.0.0_amd64.deb -O minio.deb; \
    dpkg -i minio.deb; \
    wget https://dl.min.io/client/mc/release/linux-amd64/mc; chmod +x mc; \
    mv mc /usr/local/bin/mc

SHELL ["/bin/bash", "-c"]
USER $USERNAME
WORKDIR /home/$USERNAME

# Install Scala as user
RUN wget -O sdk.install.sh "https://get.sdkman.io"; chmod +x sdk.install.sh
RUN ./sdk.install.sh; \
    source ~/.sdkman/bin/sdkman-init.sh && \
    sdk install scala 2.12.18 && \
    sdk install sbt; rm sdk.install.sh 

COPY requirements.txt ./requirements.txt
RUN pip3 install -r ./requirements.txt

ENTRYPOINT [ "/opt/entrypoint.sh" ]
