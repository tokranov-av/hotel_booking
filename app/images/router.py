import os
from pathlib import Path

import aiofiles
from fastapi import APIRouter, UploadFile

from app.tasks.tasks import process_pic

router = APIRouter(
    prefix='/images',
    tags=['Загрузка картинок']
)

base_dir = Path(__file__).resolve().parent.parent
images_dir_path = os.path.join(base_dir, 'static', 'images')


@router.post('/hotels')
async def add_hotel_image(name: int, file: UploadFile):
    """Эндпоинт загрузки изображений с последующим сжатием"""
    im_path = os.path.join(images_dir_path, f'{name}.webp')
    async with aiofiles.open(im_path, 'wb') as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk
    process_pic.delay(im_path)
    return {'result': 'OK'}
