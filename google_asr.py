import ntpath
import time

# Imports the Google Cloud client library
from google.cloud import speech_v1p1beta1 as speech
from glob import glob

"""
# FOR CLOUD
# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
gcs_uri = "gs://is457_audiofiles/common_voice_en_12.mp3"

audio = speech.RecognitionAudio(uri=gcs_uri)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.MP3,
    sample_rate_hertz=16000,
    language_code="en-US",
)

# Detects speech in the audio file
response = client.recognize(config=config, audio=audio)

for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))

"""
client = speech.SpeechClient()


def transcribe_file(speech_file):
    """Transcribe the given audio file asynchronously."""

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    """
     Note that transcription is limited to a 60 seconds audio file.
     Use a GCS file for audio longer than 1 minute.
    """
    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code="en-US",
    )


    operation = client.long_running_recognize(config=config, audio=audio)

    # print("Waiting for operation to complete...")
    response = operation.result(timeout=90)
    print(response)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        # print(response)
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))
        # print(result)

if __name__ == "__main__":
    audio_files = glob("./audio/*.mp3")
    start = time.time()

    for audio_file in audio_files:
        print("Filename:", ntpath.basename(audio_file))
        transcribe_file(audio_file)

    elapsed = time.time() - start
    avg_time = elapsed / len(audio_files)
    print("-" * 50)
    print("Average time taken:", avg_time)
