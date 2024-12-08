import os
import asyncio
from abc import ABC, abstractmethod
import aiohttp
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Config:
    FLIC_TOKEN = "<YOUR_FLIC_TOKEN>"
    UPLOAD_URL_ENDPOINT = "https://api.socialverseapp.com/posts/generate-upload-url"
    CREATE_POST_ENDPOINT = "https://api.socialverseapp.com/posts"
    VIDEO_DIRECTORY = "./videos"


class APIClient:
    def _init_(self, token):
        self.token = token

    async def get(self, url):
        headers = {"Flic-Token": self.token, "Content-Type": "application/json"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.json() if response.status == 200 else None

    async def put(self, url, data):
        headers = {"Content-Type": "video/mp4"}
        async with aiohttp.ClientSession() as session:
            async with session.put(url, data=data, headers=headers) as response:
                return response.status == 200

    async def post(self, url, json_data):
        headers = {"Flic-Token": self.token, "Content-Type": "application/json"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=json_data) as response:
                return response.status == 200


class VideoProcessor(ABC):
    @abstractmethod
    async def process(self, file_path):
        pass


class VideoUploader(VideoProcessor):
    def _init_(self, api_client):
        self.api_client = api_client

    async def process(self, file_path):
        upload_url, file_hash = await self._generate_upload_url()
        if upload_url and file_hash:
            upload_status = await self._upload_video(upload_url, file_path)
            if upload_status:
                post_status = await self._create_post(file_hash)
                if post_status:
                    os.remove(file_path)

    async def _generate_upload_url(self):
        response = await self.api_client.get(Config.UPLOAD_URL_ENDPOINT)
        return (response.get("upload_url"), response.get("hash")) if response else (None, None)

    async def _upload_video(self, upload_url, file_path):
        with open(file_path, "rb") as file:
            return await self.api_client.put(upload_url, file)

    async def _create_post(self, file_hash):
        data = {"title": "Uploaded Video", "hash": file_hash, "is_available_in_public_feed": False, "category_id": 1}
        return await self.api_client.post(Config.CREATE_POST_ENDPOINT, data)


class DirectoryMonitor:
    def _init_(self, directory, event_handler):
        self.directory = directory
        self.event_handler = event_handler

    def start(self):
        observer = Observer()
        observer.schedule(self.event_handler, self.directory, recursive=False)
        observer.start()
        try:
            while True:
                asyncio.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


class VideoEventHandler(FileSystemEventHandler):
    def _init_(self, processor):
        self.processor = processor

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".mp4"):
            asyncio.run(self.processor.process(event.src_path))


def main():
    os.makedirs(Config.VIDEO_DIRECTORY, exist_ok=True)
    api_client = APIClient(Config.FLIC_TOKEN)
    video_uploader = VideoUploader(api_client)
    event_handler = VideoEventHandler(video_uploader)
    monitor = DirectoryMonitor(Config.VIDEO_DIRECTORY, event_handler)
    monitor.start()


if __name__ == "_main_":
    main()