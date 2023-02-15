# Modify GP2 to GP3


**[Mechanism](#Mechanism)** |
**[Implementation](#Implementation)** |
![Screenshot 2022-10-30 at 11 53 34](https://user-images.githubusercontent.com/70803336/198872721-c74164d9-0737-4393-a7be-8f0ccd707600.png)


# Mechanism

The lambda find all gp2 volumes in all regions modify them to gp3 and send SNS , every day.

# Implementation

1) Upload the code to s3 bucket as a zip file.
<img width="1387" alt="Screenshot 2023-02-15 at 14 16 29" src="https://user-images.githubusercontent.com/70803336/219025094-beffbec6-de2f-4466-8e32-271c7bbfbceb.png">

2) Deploy stack via cloudformation by upload  **`CF-modify-gp2-to-gp3.yaml`**
<img width="1144" alt="Screenshot 2023-02-15 at 14 17 15" src="https://user-images.githubusercontent.com/70803336/219025271-26a714b9-fd24-4ee4-9015-f24d9d4dfd4b.png">

3) Fill the values:

<img width="1226" alt="Screenshot 2023-02-15 at 14 20 49" src="https://user-images.githubusercontent.com/70803336/219025988-625d1c35-2f24-4c60-a1b5-96182d8b4e9f.png">

* NOTE: you have to deploy the CF file in same region as the s3 bucket

## Variables

### Overview

The following variables are available in **`CF-modify-gp2-to-gp3.yaml`** and used to set up your infrastructure.

| Variable | Type | Description                                                                                                         |
|----------|------|---------------------------------------------------------------------------------------------------------------------|
| `CreateSnsTopic` | String | Do You want to create new SNS topic and subscription? if you have one and you want to use yours please answer False |
| `ExistSnsTopicArn` | String | Relevant if you have exist Topic and subscription!! Enter exist topic ARN, else do nothing                          |
| `EndpointSubscription        ` | String | Relevant if you want new Topic!! Enter your email to get SNS notification, else do nothing                          |
| `S3BucketWithCodes        ` | String | Enter the name of s3 bucket who contain the modify code for lambda function                                         |
| `YourS3keyTagZIP        ` | String | Enter name of tag zip code file in S3 bucket(From Cloudteam)                                                        |
