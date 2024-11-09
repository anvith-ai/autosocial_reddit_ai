import os
import requests
from PIL import Image
import base64
import anthropic
import re

class ImageProcessor:
    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_api_key)

    def download_image(self, url, post_id):
        try:
            response = requests.get(url)
            response.raise_for_status()

            if not os.path.exists("img"):
                os.makedirs("img")

            file_extension = os.path.splitext(url)[1]
            file_name = f"{post_id}{file_extension}"
            file_path = os.path.join("img", file_name)

            with open(file_path, "wb") as file:
                file.write(response.content)

            return file_path
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {url} - {str(e)}")
            return None

    def resize_image(self, image_path, max_size=1024):
        try:
            with Image.open(image_path) as image:
                image.thumbnail((max_size, max_size))
                resized_path = os.path.splitext(image_path)[0] + "_resized.jpg"
                image.save(resized_path, "JPEG")
                return resized_path
        except requests.exceptions.RequestException as e:
            print(f"Error resizing image: {image_path} - {str(e)}")
            return None

    def describe_image(self, image_path):
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")

        media_type = "image/jpeg"  # set the media type to "image/jpeg" for JPEG images

        message = self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Describe this image and rewrite ALL the text in the image:"
                        }
                    ],
                }
            ]
        )

        return message.content[0].text.strip()

    def process_post_image(self, post):
        if post.url and re.search(r"\.(jpg|jpeg|png|gif|bmp)$", post.url, re.IGNORECASE):
            image_path = self.download_image(post.url, post.id)
            if image_path:
                resized_path = self.resize_image(image_path)
                if resized_path:
                    return self.describe_image(resized_path)
        return ""