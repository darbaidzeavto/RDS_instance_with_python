import boto3
import requests
from os import getenv
from dotenv import load_dotenv
import argparse
import logging
from boto3.s3.transfer import TransferConfig
load_dotenv()
parser = argparse.ArgumentParser()
parser.add_argument('--secuity_group_id', "-sgi", type=str, help='vpc ID')
parser.add_argument('--subnet_group_name', "-sgn", type=str, help='subnet group name')
parser.add_argument('--DBInstanceIdentifier', "-dbi", type=str, help='DBInstanceIdentifier')

args = parser.parse_args()


def create_db_instance(rds_client, ec2_client, secuity_group_id, subnet_group_name, DBInstanceIdentifier):
  response = rds_client.create_db_instance(
    DBName='darbaidzedb',
    DBInstanceIdentifier=DBInstanceIdentifier,
    AllocatedStorage=60,
    DBInstanceClass='db.t3.micro',
    Engine='mysql',
    MasterUsername='admin',
    MasterUserPassword='admin12345',
    VpcSecurityGroupIds=[secuity_group_id],
    BackupRetentionPeriod=7,
    Port=3306,
    MultiAZ=True,
    EngineVersion='8.0.32',
    AutoMinorVersionUpgrade=True,
    PubliclyAccessible=True,
    Tags=[
      {
        'Key': 'Name',
        'Value': 'First RDS'
      },
    ],
    StorageType='gp2',
    DeletionProtection=False,
    DBSubnetGroupName=subnet_group_name)
  openPort = ec2_client.authorize_security_group_ingress(
    GroupId='sg-0c4acb0313d7ae6be',
    IpProtocol='tcp',
    FromPort=3306,
    ToPort=3306,
    CidrIp='0.0.0.0/0')
  _id = response.get("DBInstance").get("DBInstanceIdentifier")
  print(f"Instance {_id} was created")

  return response



def main():
  """The main function."""

  rds_client = boto3.client(
    'rds',
    aws_access_key_id=getenv("aws_access_key_id"),
    aws_secret_access_key=getenv("aws_secret_access_key"),
    aws_session_token=getenv("aws_session_token"),
    region_name=getenv("aws_region_name"))
  ec2_client = boto3.client(
    "ec2",
    aws_access_key_id=getenv("aws_access_key_id"),
    aws_secret_access_key=getenv("aws_secret_access_key"),
    aws_session_token=getenv("aws_session_token"),
    region_name=getenv("aws_region_name"))
  db_instance = create_db_instance(rds_client, ec2_client, args.secuity_group_id, args.subnet_group_name, args.DBInstanceIdentifier)

if __name__ == '__main__':
  main()
