from __future__ import print_function
import time
import boto3
import requests
import pandas as pd
import json

aws_access_key_id='ASIAZXDZAQL4QGQCEZ4P'
aws_secret_access_key='9zboikyRkiSBSYtsQQwC41WsXOXeOgSRnZBRzJQd'
aws_session_token='FwoGZXIvYXdzEJf//////////wEaDJjW6fjo8/M6aI6yFyLMAfdqghuQ/V1NbOmC8B+2eBt/HsnUNI8aSmUYC8Op4uIHmJmRgnOnenyujQ30Q5Ix4tqVEXgGxsmUeuMFSzIsTHPAwIFEDyPY3feUS+MVjunCV6BTVrWK0Rfq96NLTv67UibVsKRCqNa7zs84yNySwmzlew+Wf9436DS8oJysEyadX6qBYV65LHdE71yzKmR3TWaiYzBSj9qx2likkisuShJt9rxk0DnfjGgpNVYqWZHAB93QKUpBG3wN0MRkkxkDxgnD2oxXSeO+J79Y2Si5mdyKBjIt4CA6ZWhy6WCyo56vzqtTZaA7e2GzmIbzwQ6TylWZuxQiQaim3XRUD70tBWGW'

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
for obj in bucket.objects.filter(Prefix='asian/'):
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


# # Retrieve results of all transcription jobs
# for obj in bucket.objects.all():
#     job_name = obj.key
#     result = transcribe.get_transcription_job(TranscriptionJobName=job_name)
#     URI = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
#     r = requests.get(URI).json()
#     filename = str(job_name.split(".")[0]) + "-result"
#     with open(filename, 'w') as f:
#         json.dump(r,f)
#     file_name = r['jobName']
#     transcript = r['results']['transcripts'][0]['transcript']
#     print(file_name)
#     print(transcript)
#     print('-----')