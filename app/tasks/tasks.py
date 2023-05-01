import os
import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery import celery_app
from app.tasks.email_templates import create_booking_confirmation_template

base_dir = Path(__file__).resolve().parent.parent
images_dir_path = os.path.join(base_dir, 'static', 'images')


@celery_app.task
def process_pic(path: str):
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


@celery_app.task
def send_booking_confirmation_email(booking: dict, email_to: EmailStr):
    email_to_mock = 'artur.tokranov888@yandex.ru'
    msg_content = create_booking_confirmation_template(booking, email_to_mock)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
