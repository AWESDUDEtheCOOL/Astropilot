from resemble import Resemble
import os
from twilio.rest import Client
from dotenv import dotenv_values


def alert(title, body, phone_number):
    '''
    Create an alert with the given title and body
    Parameters:
        title (str): The title of the audio clip
        body (str): The text of the audio clip
        phone_number (str): The phone number to call
    '''
    env_vars = dotenv_values(".env")
    resemble_api_key = env_vars['RESEMBLE_API_KEY']
    project_uuid = env_vars['RESEMBLE_PROJECT_UUID']
    voice_uuid = env_vars['RESEMBLE_VOICE_UUID']
    Resemble.api_key(resemble_api_key) 
    response = Resemble.v2.clips.create_sync(
        project_uuid,
        voice_uuid,
        body,
        title,
        sample_rate=44100,
        output_format="mp3",
        include_timestamps=True)

    clip_uuid = response['item']['uuid']

    response = Resemble.v2.clips.get(project_uuid, clip_uuid)
    clip_url = response['item']['audio_src']
    
    account_sid = env_vars['TWILIO_ACCOUNT_SID']
    auth_token = env_vars['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    client.calls.create(
                        twiml=f'<Response><Play>{clip_url}</Play></Response>',
                        to=phone_number,
                        from_='+15595499599'
                    )
    return

def alert_clear():
    '''
    Delete all clips in the project and all files in the 'Clips' directory
    '''
    env_vars = dotenv_values(".env")
    resemble_api_key = env_vars['RESEMBLE_API_KEY']
    project_uuid = env_vars['RESEMBLE_PROJECT_UUID']
    Resemble.api_key(resemble_api_key)
    
    # Get all UUIDs and delete clips
    for item in Resemble.v2.clips.all(project_uuid, 1, 10).get('items', []):
        Resemble.v2.clips.delete(project_uuid, item['uuid'])