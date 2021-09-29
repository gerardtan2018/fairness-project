from __future__ import print_function
import time
import boto3
import requests
import pandas as pd
import json

transcribe = boto3.client('transcribe',
    aws_access_key_id='ASIA4FSAEHTG7Y7V4P5B',
    aws_secret_access_key='YqJLapISXHIyjcDK9oSdSz0hAJQlzrVcKvqgnnqH',
    aws_session_token='FwoGZXIvYXdzEDEaDALxX55hg7fcBlm72iLOAQE7r9IyNvxpp8d1W0sz9ethfv/3Tmlybhwg37Hv7KEn9i5HFHNASSJsirM9XInkyMXg7+n5ZNSbYUUcbI9dk1vkS/yp7colPP1fzS0R87rdtH5hFzc2IX2bwoxqA9LAf+p986lfR17XmzfAPkuZT/SMiNngJMwSRGlIYonaBJClZEbEzzZY4BYFGfYWXJhqO+6F2YaJrIPNwceMuvF5Mtb9t5V4a+B9aaGmXY2iHwViJKn0vHrkEpeJmOStEZ2zaNG4/zCK+TMDJFrBQ7T1KKXuxYoGMi3FNyNBIYhHqfwpa8OcohFL9UzMNKR7srTPLbMBcbyebSOmzbjh1RaXvoFbXg4=',
    region_name='us-east-1'
    )
    
s3 = boto3.resource('s3',
    aws_access_key_id='ASIA4FSAEHTG7Y7V4P5B',
    aws_secret_access_key='YqJLapISXHIyjcDK9oSdSz0hAJQlzrVcKvqgnnqH',
    aws_session_token='FwoGZXIvYXdzEDEaDALxX55hg7fcBlm72iLOAQE7r9IyNvxpp8d1W0sz9ethfv/3Tmlybhwg37Hv7KEn9i5HFHNASSJsirM9XInkyMXg7+n5ZNSbYUUcbI9dk1vkS/yp7colPP1fzS0R87rdtH5hFzc2IX2bwoxqA9LAf+p986lfR17XmzfAPkuZT/SMiNngJMwSRGlIYonaBJClZEbEzzZY4BYFGfYWXJhqO+6F2YaJrIPNwceMuvF5Mtb9t5V4a+B9aaGmXY2iHwViJKn0vHrkEpeJmOStEZ2zaNG4/zCK+TMDJFrBQ7T1KKXuxYoGMi3FNyNBIYhHqfwpa8OcohFL9UzMNKR7srTPLbMBcbyebSOmzbjh1RaXvoFbXg4='
    )
bucket = s3.Bucket('transcribe-audio-is457')

# Create trascriptions for all files in s3
for obj in bucket.objects.all():
    job_name = obj.key
    job_uri = f"s3://transcribe-audio-is457/{job_name}" 
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageOptions=['en-US','en-AU', 'en-GB', 'en-IN', 'en-WL']
    )


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