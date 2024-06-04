import requests
import json

class VideoProcessor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        self.process_url = 'https://api.mixpeek.com/tools/video/process'
        self.embed_url = 'https://api.mixpeek.com/embed'

    def process_video(self, video_url):
        payload = {
            "url": video_url,
            "frame_interval": 5,
            "resolution": [720, 1280],
            "use_base64": True
        }
        response = requests.post(self.process_url, headers=self.headers, json=payload)
        return response.json()

    def embed_video(self, base64_string):
        payload = {
            "input": base64_string,
            "modality": "video",
            "model": "mixpeek/vuse-generic-v1",
            "input_type": "base64"
        }
        response = requests.post(self.embed_url, headers=self.headers, json=payload)
        return response.json()

    def process_and_embed(self, video_url):
        processed_videos = self.process_video(video_url)
        results = []
        for index, video in enumerate(processed_videos):
            print(f"embedding video chunk: {index}")
            embed_response = self.embed_video(video['base64_string'])
            video.pop('base64_string')
            video.update(embed_response)
            results.append(video)
        return results

# Usage
api_key = 'API_KEY'
video_url = 'https://mixpeek-public-demo.s3.us-east-2.amazonaws.com/billo/117772_Scene1_16x9.mp4'
processor = VideoProcessor(api_key)
result = processor.process_and_embed(video_url)
print(json.dumps(result, indent=4))