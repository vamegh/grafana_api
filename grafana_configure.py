#!/usr/bin/python

### This is just an example script that can be used.

from grafana import grafana, config_handler

def read_yaml(config_file=''):
  with open(config_file, "r") as config:
    yaml_data = yaml.safe_load(config)
  return yaml_data

def scan_yaml(config_data=''):

yaml_data = config_handler.read_yaml(config_file='grafana_config.yaml')
database_data, grafana_data = config_handler.sanitize_yaml(config_data=yaml_data)

graf_session = grafana.GRAF(config=grafana_data)
graf_session.login()
graf_session.get_datasources()

for key in database_data:
  graf_session.post_datasource(data=database_data[key])

