#!/usr/bin/env bash
docker build -t "$1" .
docker run -d -p 5000:5000 "$1"
