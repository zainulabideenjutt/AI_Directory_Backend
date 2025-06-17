import os
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from uuid import uuid4

def download_and_save_image(image_url, folder):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113 Safari/537.36',
            'Referer': image_url  # Helps bypass some hotlink protection
        }

        print(f"Downloading image from {image_url}...")
        response = requests.get(image_url, headers=headers)
        print(f"Response status code: {response.status_code}")

        if response.status_code == 200:
            file_ext = image_url.split('.')[-1].split('?')[0]
            print(f"File extension detected: {file_ext}")
            filename = f"{uuid4()}.{file_ext}"
            path = os.path.join(folder, filename)
            default_storage.save(path, ContentFile(response.content))
            return default_storage.url(path)

    except Exception as e:
        print(f"Image download failed: {e}")
    return None
