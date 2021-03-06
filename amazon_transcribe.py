from __future__ import print_function
import time
import boto3
import requests
import pandas as pd
import json

# PLEASE FILL IN BEFORE RUNNING
aws_access_key_id=''
aws_secret_access_key=''
aws_session_token=''

transcribe = boto3.client('transcribe',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name='us-east-1'
    )
    
s3 = boto3.resource('s3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
    )

bucket = s3.Bucket('fairness-samples')

# This is used to delete all jobs
# response = transcribe.list_transcription_jobs(JobNameContains='common_voice_en',MaxResults=100)

# for job in response['TranscriptionJobSummaries']:
#     transcribe.delete_transcription_job(TranscriptionJobName=job['TranscriptionJobName'])

# while "NextToken" in response and response['NextToken'] != "":
#     response = transcribe.list_transcription_jobs(Status='FAILED',MaxResults=100, NextToken=response['NextToken'])
#     for job in response['TranscriptionJobSummaries']:
#         transcribe.delete_transcription_job(TranscriptionJobName=job['TranscriptionJobName'])  


# Create trascriptions for all files in s3
for obj in bucket.objects.filter(Prefix='non_asian/'):
    job_name = obj.key.split('/')[-1]
    job_uri = "s3://fairness-samples/" + obj.key
    try: 
        result = transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat='mp3',
            LanguageCode='en-US'
        )
        print(result['TranscriptionJob']['TranscriptionJobName'])
    except:
        pass    


# Retrieve results of all transcription jobs
for obj in bucket.objects.all():
    job_name = obj.key
    result = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    URI = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
    r = requests.get(URI).json()
    filename = str(job_name.split(".")[0]) + "-result"
    with open(filename, 'w') as f:
        json.dump(r,f)
    file_name = r['jobName']
    transcript = r['results']['transcripts'][0]['transcript']
    print(file_name)
    print(transcript)
    print('-----')
