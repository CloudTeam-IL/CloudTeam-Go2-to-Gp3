import boto3
import os

# This is the ARN of the SNS topic that you want to send the notification to.
SNS_ARN_TOPIC = os.getenv('SNS_ARN_TOPIC')


def send_sns_modify_gp2_to_gp3_volumes(gp2_volumes_list, topic_arn, region):
    """
    This function sends a message to the SNS topic that you specify in the `topic_arn` variable. The message contains the
    number of volumes that were modified and the list of volume IDs

    :param gp2_volumes_list: A list of GP2 volumes that are being converted to GP3
    :param topic_arn: The ARN of the SNS topic to send the notification to
    :param region: The region where the volumes are located
    """
    sns_client = boto3.client('sns')
    message = f"The lambda upgrade {len(gp2_volumes_list)} GP2 volumes: {gp2_volumes_list} in {region} by CloudTeam Lambda (Moidfy GP2 to GP3)."
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )


def list_gp2_volumes(ec2_client):
    """
    This function will return a list of all gp2 volumes in the account

    :param ec2_client: The boto3 client object for EC2
    :return: A list of gp2 volumes
    """
    describe_volumes = ec2_client.describe_volumes(Filters=[{"Name": "volume-type", "Values": ["gp2"]}])
    gp2_list = []

    for vol in describe_volumes["Volumes"]:
        print("gp2 volume found = {VolumeId}".format(**vol))
        gp2_list.append(vol["VolumeId"])
    return gp2_list


def modify_gp2_volumes(ec2_client, gp2_volumes_list):
    """
    This function takes a list of gp2 volume IDs and modifies them to gp3

    :param ec2_client: The boto3 client object for EC2
    :param gp2_volumes_list: A list of volume IDs that you want to convert to gp3
    """
    try:
        for vol in gp2_volumes_list:
            ec2_client.modify_volume(VolumeId=vol, VolumeType="gp3")
            print(f"Instance modified: {vol}")
    except boto3.exceptions.botocore.client.ClientError as e:
        print(e.response["Error"]["Message"].strip("\""))


def lambda_handler(event, context):
    ec2_client = boto3.client("ec2")
    """
    The function loops through all the regions, and for each region, it lists all the gp2 volumes, and if there are any,
    it modifies them to gp3 volumes, and sends an SNS notification

    :param event: This is the event that triggered the lambda function
    :param context: The runtime information provided by Lambda.
    """
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    for region in regions:
        print(f'Region: {region}')
        ec2_client = boto3.client('ec2', region_name=region)
        gp2_volumes_list = list_gp2_volumes(ec2_client)
        if gp2_volumes_list:
            print(gp2_volumes_list)
            modify_gp2_volumes(ec2_client, gp2_volumes_list)
            send_sns_modify_gp2_to_gp3_volumes(gp2_volumes_list, SNS_ARN_TOPIC, region)
