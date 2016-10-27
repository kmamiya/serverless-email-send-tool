#! /usr/bin/env python
# -*- coding: utf-8
#
# ConoHa; The library for ConoHa ( https://www.conoha.jp/conoha/ ) API.
#
# Copyright (c) 2016 Kentarou Mamiya See LICENSE for details.
#   Website; http://logicalrabbit.jp/ 
#
# This file is built for simply execution.

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

import sys
import json
from smtplib import SMTP
from email.mime.text import MIMEText

def exit_if_failure( conoha ):
    if not conoha.success():
        print( 'HTTP_STATUS: ' + str( conoha.http_status() ) )
        exit( 1 )

def sendmail( smtp, from_addr, to_addr, subject, mailbody ):
    message = MIMEText( mailbody )
    message['Subject'] = subject
    message['From']    = from_addr
    message['To']      = to_addr

    ma.sendmail( from_addr, to_addr, message.as_string() )


# Main routine start.
#
# Usage: notify_mail.py <config.json> <subject> <mailbody.txt>
#   subject          ... The notify mail subject.
#   mailbody.txt     ... The notify mail body.
#
# (Bash only)
# If you want to send the simple message, can use the process substitution.
# e.g. $ notify_mail.py config.json 'Report' <(echo 'simple message')
# 

if 4 > len( sys.argv ):
    print( 'Usage: notify_mail.py <config.json> <subject> <mailbody.txt>' )
    exit( 1 )

with open( sys.argv[1], 'r' ) as config_reader:
    config = json.loads( config_reader.read() )

conoha = ConoHa( config['identity_url'], config['user_agent'] )

connect_response = conoha.connect(
    config['username'], config['password'], config['tenant_id']
)
exit_if_failure( conoha )

# Set the mail service name (Notify) and default_domain (notify).
# default_domain is use for sender mail address.
mail_info = conoha.create_mail_service( 'NotifyMail', 'notify' )
exit_if_failure( conoha )

mail_service_id     = mail_info['service']['service_id']
mail_default_domain = mail_info['service']['default_domain']

mail_domain_info = conoha.list_mail_domain( mail_service_id )
exit_if_failure( conoha )

from_address = config['mail_account'] + '@' + mail_default_domain

creation_email = conoha.create_mail_address(
    mail_domain_info[mail_default_domain]['domain_id'],
    from_address, config['mail_password']
)
exit_if_failure( conoha )

with open( sys.argv[3], 'r' ) as mailbody_reader:
    mailbody = mailbody_reader.read()

ma = SMTP()
ma.connect( mail_info['service']['smtp'] )
ma.login( from_address, config['mail_password'] )
sendmail( ma, from_address, config['mail_to'], sys.argv[2], mailbody )

delete_result = conoha.delete_mail_service( mail_service_id )

exit( len( conoha.list_mail_service() ) )
