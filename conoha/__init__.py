# -*- coding: utf-8
#
# ConoHa; The library for ConoHa ( https://www.conoha.jp/conoha/ ) API.
#
# Copyright (c) 2016 Kentarou Mamiya See LICENSE for details.
#   Website; http://logicalrabbit.jp/ 
#

import json
import urllib2
from urllib2 import urlopen
from urllib2 import HTTPError
from urlparse import urljoin

class ConoHa:
    'The library for ConoHa API.'

    def __init__( self, identity_url, user_agent ):
        """\
Constructor.

identity_url ... Please check your ConoHa dashboard.
                 (API tab -> endpoint -> Identity Service)
user_agent   ... Ex. Any name and contact URL.
"""
        self.auth_info    = {}
        self.auth_headers = {}
        self.endpoints    = {}
        self.http_status  = 0

        self.user_agent = user_agent
        self.identity_url = urljoin( identity_url, '/' )

    def http_status( self ):
        'HTTP_STATUS value of last access.'

        return self.http_status

    def success( self ):
        'The HTTP_STATUS of last access is 200 or not.'

        return ( 200 == self.http_status )
 
    def mailhosting_endpoint( self ):
        """\
The Mail Service endpoint URI.

This value get from the token request result.
"""
        return self.endpoints['mailhosting']['endpoints'][0]['publicURL']

    def imageservice_endpoint( self ):
        return 'https://image-service.tyo1.conoha.io'

    def connect( self, username, password, tenant_id ):
        """\
Start connection to ConoHa API.

    username  ... API user name. (This isn't ConoHa account)
    password  ... API user password. (This isn't ConoHa account)
    tenant_id ... (on dashboard)API info. ->tenant info. -> tenant ID.
"""
        postdata = json.dumps( {
            'auth': {
                'passwordCredentials': {
                    'username': username,
                    'password': password
                },
                'tenantId': tenant_id
            }
        } )

        try:
            response = urlopen( urllib2.Request(
                urljoin( self.identity_url, '/v2.0/tokens' ),
                postdata,
                {
                    'Accept': 'application/json',
                    'User-Agent': self.user_agent
                }
            ) )
            self.http_status = response.getcode()
            if self.success():
                self.auth_info = json.loads( response.read() )
                response.close()
                self.auth_headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'User-Agent': self.user_agent,
                    'X-Auth-Token': self.auth_info['access']['token']['id']
                }
                for endpoint in self.auth_info['access']['serviceCatalog']:
                  self.endpoints[endpoint['type']] = endpoint

                return {
                    'auth_info': self.auth_info,
                    'auth_headers': self.auth_headers
                }
            else:
                response.close()
                return self.http_status

        except HTTPError as err:
            self.http_status = err.code
            return self.http_status
        else:
            response.close()

    def list_mail_service( self ):
        'https://www.conoha.jp/docs/paas-mail-list-mail-service.html'

        try:
            response = urlopen( urllib2.Request(
                urljoin( self.mailhosting_endpoint(), '/v1/services' ),
                None,
                self.auth_headers
            ) )
            self.http_status = response.getcode()
            if self.success():
                infos = json.loads( response.read() )

                service_info = {}
                for info in infos['services']:
                    service_info[info['service_name']] = info
                response.close()

                return service_info
            else:
                response.close()
                return self.http_status
        except HTTPError as err:
            self.http_status = err.code
            return self.http_status
        else:
            response.close()

    def create_mail_service( self, service_name, default_sub_domain ):
        'https://www.conoha.jp/docs/paas-mail-create-mail-service.html'

        postdata = json.dumps( {
            'service_name': service_name,
            'default_sub_domain': default_sub_domain
        } )
        try:
            response = urlopen( urllib2.Request(
                urljoin( self.mailhosting_endpoint(), '/v1/services' ),
                postdata,
                self.auth_headers
            ) )
            self.http_status = response.getcode()
            if self.success():
                info = json.loads( response.read() )
                response.close()

                return info
            else:
                response.close()
                return self.http_status
        except HTTPError as err:
            self.http_status = err.code
            return self.http_status
        else:
            response.close()

    def delete_mail_service( self, service_id ):
        'https://www.conoha.jp/docs/paas-mail-delete-mail-service.html'

        try:
            request = urllib2.Request(
                urljoin(
                    self.mailhosting_endpoint(),
                    ('/v1/services/' + service_id)
                ),
                None,
                self.auth_headers
            )
            request.get_method = lambda: 'DELETE'
            response = urlopen( request )

            self.http_status = response.getcode()
            response.close()

            return self.http_status
        except HTTPError as err:
            self.http_status = err.code
            return self.http_status
        else:
            response.close()

    def list_mail_domain( self, service_id ):
        'https://www.conoha.jp/docs/paas-mail-list-domain.html'

        try:
            response = urlopen( urllib2.Request(
                urljoin( self.mailhosting_endpoint(), '/v1/domains' ),
                None,
                self.auth_headers
            ) )
            self.http_status = response.getcode()
            if self.success():
                infos = json.loads( response.read() )

                domain_info = {}
                for info in infos['domains']:
                    domain_info[info['domain_name']] = info

                response.close()

                return domain_info
            else:
                response.close()
                return self.http_status
        except HTTPError as err:
            self.http_status = err.code
            return self.http_status
        else:
            response.close()

    def create_mail_address( self, domain_id, email, account_password ):
        'https://www.conoha.jp/docs/paas-mail-create-email.html'

        postdata = json.dumps( {
            'domain_id': domain_id,
            'email': email,
            'password': account_password
        } )
        try:
            response = urlopen( urllib2.Request(
                urljoin( self.mailhosting_endpoint(), '/v1/emails' ),
                postdata,
                self.auth_headers
            ) )
            self.http_status = response.getcode()
            if self.success():
                info = json.loads( response.read() )
                response.close()

                return info
            else:
                response.close()
                return self.http_status
        except HTTPError as err:
            self.http_status = err.code
            return self.http_status
        else:
            response.close()

    def list_image( self ):
        try:
            response = urlopen( urllib2.Request(
                urljoin( self.imageservice_endpoint(), '/v2/images' ),
                None,
                self.auth_headers
            ) )
            self.http_status = response.getcode()
            if self.success():
                infos = json.loads( response.read() )

                image_info = {}
                for info in infos['images']:
                    image_info[info['name']] = info

                response.close()

                return image_info
            else:
                response.close()
                return self.http_status
        except HTTPError as err:
            self.http_status = err.code
            return self.http_status
        else:
            response.close()

