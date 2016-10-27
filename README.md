# serverless-email-send-tool
The tool for send mail without SMTP server (Using ConoHa API)

You need ConoHa ( https://www.conoha.jp/conoha/ ) account for this tool use.

# Install

1. `git clone git@github.com:kmamiya/serverless-email-send-tool.git`
2. `cd serverless-email-send-tool/bin`
3. rename or copy from config.json.template
4. edit config.json 
5. `./notify_mail.py config.json 'Mail subject' <(echo 'Hello')` (on bash)

# How to use

I think the following use case;

- (On OS initialize, I wait long long time for yum upgrade...) `$ sudo yum -y upgrade ; ./notify_mail.py config.json 'Report from server' <(echo 'yum upgrade finished')`
- (On application complie) `$ make ; ./notify__mail.py config.json 'Report from server' <(make check; echo $?)`

# Website (Japanese)

http://logicalrabbit.jp/serverless-email-send-tool

# LICENSE

Copyright (c) 2015 Kentarou Mamiya. See LICENSE for details. 
