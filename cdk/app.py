#!/usr/bin/env python3

import aws_cdk as cdk
from cdk_stack import UnemploymentMLStack

app = cdk.App()

UnemploymentMLStack(app, "UnemploymentMLStack")

app.synth()
