#!/bin/bash

project=Clasp/Overview

current_deployment=$(clasp deployments --project "${project}" | tail -n1 | cut -d' ' -f2)

clasp push --project "${project}"
clasp deploy --project "${project}" --deploymentId "${current_deployment}"
