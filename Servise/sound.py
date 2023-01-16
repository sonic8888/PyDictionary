import logging
from os import path
import requests
from Servise.tools import display_error, Settings

logging_sound = logging.getLogger(__name__)
logging_sound.setLevel(logging.INFO)
_handler = logging.FileHandler(f'logs\\{__name__}.log', mode='w')
_formatter = logging.Formatter("%(name)s %(lineno)d %(asctime)s %(levelname)s %(message)s")
_handler.setFormatter(_formatter)
logging_sound.addHandler(_handler)


def synthesize(folder_id, iam_token, text):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': 'Bearer ' + iam_token,
    }

    data = {
        'text': text,
        'lang': 'en-US',
        'voice': 'john',
        'folderId': folder_id,
        'format': 'mp3',
        'sampleRateHertz': 48000,
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk


def get_word_sound(word, folder_id, iam_token):
    s = Settings()
    path_name = s.path_name_audio_temp + f'\\{word}.mp3'
    if not path.exists(path_name):
        response = None
        try:
            response = synthesize(folder_id, iam_token, word)
        except RuntimeError as ru:
            display_error(ru)
            logging_sound.exception(ru)
            return
        with open(path_name, "wb") as f:
            for audio_content in response:
                f.write(audio_content)
    return path_name
