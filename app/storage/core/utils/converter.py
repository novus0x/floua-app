########## Modules ##########
import os, json, subprocess, requests, asyncio

from pathlib import Path
from asyncio import Queue

from core.config import settings

########## Variables ##########
queue = Queue()

########## Valid audio  ##########
def get_valid_streams(input_file):
    try:
        ### Get video info
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', input_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        info = json.loads(result.stdout)
        audio_exists = False
        video_exists = False

        for stream in info.get("streams", []):
            codec_type = stream.get("codec_type", "")
            if codec_type == "video":
                video_exists = True
            elif codec_type == "audio":
                audio_exists = True

        return video_exists, audio_exists

    except Exception as e:
        return False, False

########## HLS converter  ##########
async def hls_converter(video_data):
    # print(video_data)
    output_dir = video_data["dir"]
    has_video, has_audio = get_valid_streams(str(video_data["video_dir"]))

    if not os.path.exists(video_data["dir"]) or not has_video:
        print("[-] Error", has_audio, has_video)
        return False

    command = [
        "ffmpeg", "-i", str(video_data["video_dir"]),
        "-filter:v:0", "scale=w=1280:h=720", "-b:v:0", "3000k",
        "-filter:v:1", "scale=w=1920:h=1080", "-b:v:1", "6000k",
        "-c:v", "h264"
    ]

    if has_audio:
        command += ["-c:a", "aac", "-strict", "-2"]
        command += ["-map", "0:v", "-map", "0:a", "-map", "0:v", "-map", "0:a"]
        command += ["-var_stream_map", "v:0,a:0 v:1,a:1"]
        print("[+] Audio")
    else:
        command += ["-map", "0:v", "-map", "0:v"]
        command += ["-var_stream_map", "v:0 v:1"]
        print("[-] Audio")

    command += [
        "-f", "hls",
        "-hls_time", "6",
        "-hls_list_size", "0",
        "-master_pl_name", "master.m3u8",
        "stream_%v.m3u8"
    ]

    process = await asyncio.create_subprocess_exec(
        *command, cwd=output_dir,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    if process.returncode == 0:
        return True
    else:
        return False


########## Video  ##########
async def video_converter():
    while True:

        data = await queue.get()

        result = await hls_converter(data)
        
        data = {
            "video_id": data["video_id"],
            "status": 400
        }

        if result:
            data["status"] = 201

        # request.post(settings.CDN_ORIGIN + "/nodes/video_status", json=data)

        queue.task_done()
