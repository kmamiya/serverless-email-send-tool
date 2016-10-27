from conoha import ConoHa

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
