#!/bin/bash

cp ./blum.docker.service /etc/systemd/system
systemctl daemon-reload
systemctl enable blum.docker.service