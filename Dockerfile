# set base image (host OS)
FROM python:3.8

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get -y update
RUN apt-get install -y curl nano wget nginx git

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list


# Mongo
RUN ln -s /bin/echo /bin/systemctl
RUN wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | apt-key add -
RUN echo "deb http://repo.mongodb.org/apt/debian bookworm/mongodb-org/7.0 main" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
RUN apt-get -y update
RUN apt-get install -y mongodb-org

# Node.js 16: react-scripts 4 (webpack 4, postcss 8.1) does not run on Node 17+
ENV NODE_VERSION 16.20.2
RUN NODE_ARCH=$(dpkg --print-architecture | sed 's/amd64/x64/') && \
    curl -fsSL https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-${NODE_ARCH}.tar.xz \
    | tar -xJ -C /usr/local --strip-components=1 --no-same-owner --exclude='*.md' --exclude=LICENSE

# Install Yarn (skip recommended distro nodejs, which is Node 18 on bookworm)
RUN apt-get install -y --no-install-recommends yarn

# Install PIP
RUN pip install "pip<24.1"


ENV ENV_TYPE staging
ENV MONGO_HOST mongo
ENV MONGO_PORT 27017
##########

ENV PYTHONPATH=$PYTHONPATH:/src/

# copy the dependencies file to the working directory
COPY src/requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the source code (kept in sync during development by `docker compose watch`)
COPY src /src
