#!/usr/bin/env bash

dnf install -y gcc-c++ make
curl -sL https://rpm.nodesource.com/setup_13.x | sudo -E bash -
dnf install nodejs
npm install -g newman