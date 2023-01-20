#!/bin/bash

#These are your config settings and must be filled out prior to executing the script. 
#You can find this info in the AWS IAM Console under your user account 'Security Credentials'
#Once you are ready, the script must executable via 'chmod +x finlename.sh'
#Then run the script with 'source filename.sh'

IAM_USER_ACCOUNT=iam-user-account
MFA_TOKEN=token-from-authenticator
MFA_SERIAL_NUM=iam-mfa-serial-num
file_path="/tmp/data.json"

#Get session token from AWS
aws sts get-session-token --serial-number $MFA_SERIAL_NUM --token-code $MFA_TOKEN >> $file_path
if [ $? -ne 0 ]; then
  echo "Error: Failed to get session token from AWS"
  exit 1
fi

#Extract credentials as env vars
AccessKeyId=$(jq -r '.Credentials.AccessKeyId' $file_path)
SecretAccessKey=$(jq -r '.Credentials.SecretAccessKey' $file_path)
SessionToken=$(jq -r '.Credentials.SessionToken' $file_path)

#Export credentials as env vars
export AWS_ACCESS_KEY_ID=$AccessKeyId
export AWS_SECRET_ACCESS_KEY=$SecretAccessKey
export AWS_SESSION_TOKEN=$SessionToken

#Remove json file
if test ! -f $file_path; then
  echo "Error: ${file_path} not found"
  exit 1
fi
rm $file_path