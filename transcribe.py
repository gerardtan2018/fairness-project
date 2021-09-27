from __future__ import print_function
import time
import boto3
import requests
import pandas as pd
transcribe = boto3.client('transcribe',
    aws_access_key_id='ASIA4FSAEHTGTI3LHWC5',
    aws_secret_access_key='EEJxkvXkmLAhG27dp7EsEcHCz6wgEZEjryPKsKaG',
    aws_session_token='FwoGZXIvYXdzEC8aDImZAvBfqelnVpvMrCLOAdHTEnafU2z/N2nc5tptapEkpwYWWY2WVqbt5wjZI5JHIIMb8c0sbk/fky/Q7LF88/uOwqum/l0rroRjI+tHN21sQYAh3nvrw8fv9UMOTSrD7cb76zMGGrgHzOyzjiAqksdHjOXpm9Yq6u5C9JhYQGRQUAJtAraN7InTNPD02xoIMi0JlSC0Bho2MJg1PfxGITmYOUtLxmP9IhJdqbxrT7yu28AOlBPqeBsOomnZd9yH2UKqpbdvGdHZxzNarUyBJxO/SJhIjjPXHLAVnuB0KLu9xYoGMi0wzUXvtzm0nxHM1U1jSfiJKXP5fzzclbjOfoOJjDj6dvnl9ipGtrztRXkw+Tk='
    )
s3 = boto3.resource('s3',
    aws_access_key_id='ASIA4FSAEHTGTI3LHWC5',
    aws_secret_access_key='EEJxkvXkmLAhG27dp7EsEcHCz6wgEZEjryPKsKaG',
    aws_session_token='FwoGZXIvYXdzEC8aDImZAvBfqelnVpvMrCLOAdHTEnafU2z/N2nc5tptapEkpwYWWY2WVqbt5wjZI5JHIIMb8c0sbk/fky/Q7LF88/uOwqum/l0rroRjI+tHN21sQYAh3nvrw8fv9UMOTSrD7cb76zMGGrgHzOyzjiAqksdHjOXpm9Yq6u5C9JhYQGRQUAJtAraN7InTNPD02xoIMi0JlSC0Bho2MJg1PfxGITmYOUtLxmP9IhJdqbxrT7yu28AOlBPqeBsOomnZd9yH2UKqpbdvGdHZxzNarUyBJxO/SJhIjjPXHLAVnuB0KLu9xYoGMi0wzUXvtzm0nxHM1U1jSfiJKXP5fzzclbjOfoOJjDj6dvnl9ipGtrztRXkw+Tk='
)
bucket = s3.Bucket('transcribe-audio-is457')

# Create trascriptions for all files in s3
# for obj in bucket.objects.all():
    # job_name = obj.key
    # job_uri = f"s3://transcribe-audio-is457/{job_name}" 
    # transcribe.start_transcription_job(
    #     TranscriptionJobName=job_name,
    #     Media={'MediaFileUri': job_uri},
    #     MediaFormat='mp3',
    #     LanguageCode='en-US'
    # )


# Retrieve results of all transcription jobs
for obj in bucket.objects.all():
    job_name = obj.key
    result = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    URI = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
    r = requests.get(URI).json()
    file_name = r['jobName']
    transcript = r['results']['transcripts'][0]['transcript']
    print(file_name)
    print(transcript)
    print('-----')