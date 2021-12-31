# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 20:51:43 2020

@author: ruben
"""
import os
from datetime import datetime

import yaml
from dotmap import DotMap

def process_config(yml_file):
    # parse the configurations from the config json file provided
    with open(yml_file, "r") as config_file:
        config_dict = yaml.load(config_file, Loader=yaml.FullLoader)

    # convert the dictionary to a namespace using bunch lib
    config = DotMap(config_dict)

    return config
