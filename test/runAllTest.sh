#!/usr/bin/env bash

newman run test/politic-center.postman_collection.json -e test/QA.postman_environment.json
