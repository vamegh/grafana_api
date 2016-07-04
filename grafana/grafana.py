#!/usr/bin/python
#
##
##########################################################################
#                                                                        #
#       Grafana API Library                                              #
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

import json
import requests
import sys
import os

class GRAF(object):
  def __init__(self, config=''):
    try:
      self.g_user = config["login_user"]
    except KeyError as e:
      print ('''Configurations should be passed as a dict,
                containing login_pass, login_user, host and port key/values''')
      sys.exit(1)
    try:
      self.g_pass = config["login_pass"]
    except KeyError as e:
      print ('''Configurations should be passed as a dict,
                containing login_pass, login_user, host and port key/values''')
      sys.exit(1)
    try:
      self.g_host = config["host"]
    except KeyError as e:
      print ('''Configurations should be passed as a dict,
                containing login_pass, login_user, host and port key/values''')
      sys.exit(1)
    try:
      self.g_port = config["port"]
    except KeyError as e:
      print ('''Configurations should be passed as a dict,
                containing login_pass, login_user, host and port key/values''')
      sys.exit(1)
    try:
      self.verify = config["ssl_verify"]
    except KeyError as e:
      self.verify = False

    grafana_url = os.path.join('http://', '%s:%s' % (self.g_host, self.g_port))
    self.login_url = grafana_url + '/login'
    self.query_url = grafana_url + '/api/datasources'
    self.post_url = grafana_url + '/api/datasources'
    self.auth_headers = {'Content-type': 'application/x-www-form-urlencoded' , 'accept': 'text/plain'}
    self.auth_payload = {'user': self.g_user, 'password': self.g_pass}
    self.query_headers = {'Content-type': 'application/json' , 'accept': 'application/json'}
    self.post_headers = {'Content-type': 'application/json' , 'accept': 'application/json'}
    self.session = ''

  def login(self):
    try:
      self.session = requests.post(self.login_url, headers=self.auth_headers, data=self.auth_payload, verify=self.verify )
    except self.session.ConnectionError as e:
      print ("Connection error :: ", str(e))
      sys.exit(1)
    except self.session.HTTPError as e:
      print ("HTTP Response error :: ", str(e))
      sys.exit(1)
    except Exception as e:
      print ("login :: error :: ", str(e))
      sys.exit(1)
    except:
      print ("login :: error :: ", sys.exc_info()[0])
      raise
    status_code = self.session.status_code
    if status_code == 401:
      print ("Auth Error could not login using auth provided :: status:",status_code,":: user:",self.i_user)
      sys.exit(1)
    elif status_code ==500:
      print ("Internal Server Error -- Service probably down :: status :: ",status_code)
      sys.exit(1)
    return "success"

  def get_datasources(self):
    payload = {}
    try:
      raw_response = requests.get(self.query_url,
                                  headers=self.query_headers,
                                  cookies=self.session.cookies,
                                  json=(payload))
    except Exception as e:
      print ("get_datasources :: error :: ", str(e))
      sys.exit(1)
    except:
      print ("get_datasources :: error :: ", sys.exc_info()[0])
      raise
    json_data = raw_response.json()
    for data in json_data:
      print ("Current DataSources:", data)

  def post_datasource(self, data=''):
    payload = { 'access': data['access'],
                'database': data['database'],
                'name': data['name'],
                'type': data['type'],
                'url': 'http://%s:%s' % (data['host'], data['port']),
                'user': data['user'],
                'password': data['password'] }
                #'isDefault': data['default'] }
    try:
       raw_response = requests.post(self.post_url,
                                    headers=self.post_headers,
                                    cookies=self.session.cookies,
                                    verify=self.verify,
                                    json=(payload))
    except Exception as e:
      print ("error :: ", str(e))
      sys.exit(1)
    except:
      print ("error :: ", sys.exc_info()[0])
      raise
    json_data = raw_response.json()
    for data in json_data:
      print ("DataSources Addition Response: ", data)

