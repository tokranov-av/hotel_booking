import os
from pathlib import Path

from PIL import Image

from app.tasks.celery import celery_app

base_dir = Path(__file__).resolve().parent.parent
images_dir_path = os.path.join(base_dir, 'static', 'images')


@celery_app.task
def process_pic(path: str,):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_1000_500.save(
        f'{images_dir_path}/resized_1000_500_{im_path.name}'
    )
    im_resized_200_100 = im.resize((200, 100))
    im_resized_200_100.save(
        f'{images_dir_path}/resized_200_100_{im_path.name}'
    )
