from resemble import Resemble
import urllib.request
import os

PROJECT_UUID = 'b7e7278f'
VOICE_UUID = 'b2d1bb75'

def alert(title, body):
    '''
    Create an alert with the given title and body
    Parameters:
        title (str): The title of the audio clip
        body (str): The text of the audio clip
    Returns:
        clip_name (str): The name of the audio clip created
    '''
    Resemble.api_key('s0GLLI9cOhTOq8qMdFH3gQtt') 
    response = Resemble.v2.clips.create_sync(
        PROJECT_UUID,
        VOICE_UUID,
        body,
        title,
        sample_rate=44100,
        output_format="wav",
        include_timestamps=True)

    clip_uuid = response['item']['uuid']

    response = Resemble.v2.clips.get(PROJECT_UUID, clip_uuid)
    clip_url = response['item']['audio_src']
    clip_name = clip_url.split('/')[-1]
    urllib.request.urlretrieve(clip_url, f'Clips/{clip_name}')
    return clip_name

def alert_clear():
    '''
    Delete all clips in the project and all files in the 'Clips' directory
    '''
    Resemble.api_key('s0GLLI9cOhTOq8qMdFH3gQtt') 
    page_size = 10
    
    # Get all UUIDs and delete clips
    for item in Resemble.v2.clips.all(PROJECT_UUID, page=1, page_size=page_size).get('items', []):
        Resemble.v2.clips.delete(PROJECT_UUID, item['uuid'])
    
    # Delete all files in 'Clips' directory
    for filename in os.listdir('Clips'):
        os.unlink(os.path.join('Clips', filename))