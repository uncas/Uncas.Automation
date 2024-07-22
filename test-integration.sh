#!/bin/bash

source init.sh

python -m unittest discover -s easai -p *IntegrationTests.py
