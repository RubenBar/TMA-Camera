# -*- coding: utf-8 -*-

import os
from datetime import datetime

import yaml
from dotmap import DotMap

def process_config(yml_file):
    # Parse the configurations from the config json file provided
    with open(yml_file, "r") as config_file:
        config_dict = yaml.load(config_file, Loader=yaml.FullLoader)

    # Convert the dictionary to a namespace using bunch lib
    config = DotMap(config_dict)

    return config
