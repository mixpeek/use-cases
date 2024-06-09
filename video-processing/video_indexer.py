from mixpeek import Mixpeek


mixpeek = Mixpeek('API_KEY')
video_url = 'https://mixpeek-public-demo.s3.us-east-2.amazonaws.com/media-analysis/The+Third+Man++Official+Trailer.mp4'

processed_videos = mixpeek.tools.video.process(
    url=video_url,
    frame_interval=5,
    resolution=[720, 1280],
    return_base64=True
)
results = []
for index, video in enumerate(processed_videos):
    print(f"embedding video chunk: {index}")
    embedding = mixpeek.embed.video(
        model_id="mixpeek/vuse-generic-v1",
        input=video['base64_string'],
        input_type="base64"
    )
    video.pop('base64_string')
    video.update(embedding)
    results.append(video)

print(results)