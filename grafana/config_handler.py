#!/usr/bin/python
#
##
##########################################################################
#                                                                        #
#       Grafana API Library :: config_handler                            #
#                                                                        #
#       (c) 2016 Vamegh Hedayati                                         #
#                                                                        #
#       Vamegh Hedayati <gh_vhedayati AT ev9 DOT io>                     #
#                                                                        #
#       Please see Copying for License Information                       #
#                             GNU/LGPL v2                                #
##########################################################################
##
#
import yaml
import sys
import os.path

def read_yaml(config_file=''):
  with open(config_file, "r") as config:
    yaml_data = yaml.safe_load(config)
  return yaml_data

def sanitize_yaml(config_data=''):
  database_config = {}
  grafana_config = {}

  for key in config_data:
    if key == "databases":
      database_config = config_data[key]
    if key == "grafana_details":
      grafana_config = config_data[key]

  for key in grafana_config:
    try:
      name = grafana_config["login_user"]
    except KeyError as e:
      new_key = e.args[0]
      grafana_config[new_key] = "admin"
    try:
      name = grafana_config["login_pass"]
    except KeyError as e:
      new_key = e.args[0]
      grafana_config[new_key] = "admin"
    try:
      name = grafana_config["host"]
    except KeyError as e:
      new_key = e.args[0]
      grafana_config[new_key] = "localhost"
    try:
      name = grafana_config["port"]
    except KeyError as e:
      new_key = e.args[0]
      grafana_config[new_key] = "admin"

  for key in database_config:
    try:
      name = database_config[key]["name"]
    except KeyError as e:
      new_key = e.args[0]
      database_config[key][new_key] = "none"
    try:
      command = database_config[key]["access"]
    except KeyError as e:
      new_key = e.args[0]
      database_config[key][new_key] = "none"
    try:
      output_variable = database_config[key]["database"]
    except KeyError as e:
      new_key = e.args[0]
      database_config[key][new_key] = "none"
    try:
      position = database_config[key]["type"]
    except KeyError as e:
      new_key = e.args[0]
      database_config[key][new_key] = "none"
    try:
      position = database_config[key]["host"]
    except KeyError as e:
      new_key = e.args[0]
      database_config[key][new_key] = "none"
    try:
      position = database_config[key]["port"]
    except KeyError as e:
      new_key = e.args[0]
      database_config[key][new_key] = "none"
    try:
      position = database_config[key]["user"]
    except KeyError as e:
      new_key = e.args[0]
      database_config[key][new_key] = ''
    try:
      position = database_config[key]["password"]
    except KeyError as e:
      new_key = e.args[0]
      database_config[key][new_key] = ''
    try:
      position = database_config[key]["default"]
    except KeyError as e:
      new_key = e.args[0]
      database_config[key][new_key] = False

  return database_config, grafana_config


