#!/bin/bash

source init.sh

python -m unittest discover -s Source -p *IntegrationTests.py
