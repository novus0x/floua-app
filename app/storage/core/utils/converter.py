########## Modules ##########
import os, shutil, json, subprocess, asyncio

from pathlib import Path
from asyncio import Queue

from core.config import settings
from core.utils.http_requests import post_data_api
from core.utils.video_detector import is_mobile_video

from services.media.main import delete_file, upload_files

########## Variables ##########
queue = Queue()

########## Valid audio  ##########
def get_valid_streams(input_file):
    try:
        ### Validate ###
        if not os.path.exists(input_file):
            print("File does not exist")
            return False, False

        ### Get video info
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', input_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )

        # ['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', input_file],

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
        print(e)
        return False, False

########## HLS converter  ##########
async def hls_converter(video_data):
    # print(video_data)
    output_dir = video_data["dir"]
    # is_mobile = is_mobile_video(str(video_data["video_dir"]))

    # # has_video, has_audio = get_valid_streams(str(video_data["video_dir"]))

    # # if not os.path.exists(video_data["dir"]) or not has_video:
    # #     print("[-] Error", has_audio, has_video)
    # #     return False
    print("[+] Reparing video")
    command = [
            "ffmpeg", "-fflags", "+genpts", "-err_detect", "ignore_err", "-i", str(video_data["video_dir"]), "-c", "copy", "-movflags", "+faststart", f"{output_dir}/temp.mp4",
    ]

    #     "ffmpeg",
    # "-err_detect", "ignore_err",  # Ignora errores y continúa
    # "-i", str(video_data["video_dir"]),
    # "-c", "copy",  # Copia los streams sin recodificar
    # "-movflags", "+faststart",  # Mueve el moov al inicio
    # f"{output_dir}/temp.mp4",

    # "ffmpeg", "-i", str(video_data["video_dir"]), "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", f"{output_dir}/temp.mp4",

    repair = await asyncio.create_subprocess_exec(
        *command, cwd=output_dir,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await repair.communicate()

    if stdout:
        print("Stdout: \n", stdout.decode())
    if stderr:
        print("Stderr: \n", stderr.decode())

    await repair.wait()

    print("Replace")
    os.replace(f"{output_dir}/temp.mp4", str(video_data["video_dir"]))
    

    # # segment_patter = os.path.join(output_dir, "stream_%v_%03d.ts")
    # # playlist_patter = os.path.join(output_dir, "stream_%v.m3u8")
    # # master_playlist = os.path.join(output_dir, "master.m3u8")

    # # print("before command")
    # print("To HLS")

    # command = [
    #     "ffmpeg", "-i", str(video_data["video_dir"]), "-filter_complex",
    #     "[0:v]split=2[v1][v2]; [v1]scale=w=1280:h=720:force_original_aspect_ratio=decrease[v1out]; [v2]scale=w=1920:h=1080:force_original_aspect_ratio=decrease[v2out]",
    #     "-map", "[v1out]", "-map", "0:a?", "-c:v:0", "libx264", "-b:v:0 3000k", "-c:a:0", "aac", "-b:a:0", "128k", "-ac:0", "1", 
    #     "-map", "[v2out]", "-map", "0:a?", "-c:v:1", "libx264", "-b:v:1", "6000k", "-c:a:1", "aac", "-b:a:1", "128k", "-ac:1", "1", 
    #     "-hls_flags", "independent_segments", 
    #     "-hls_time", "6", "-hls_playlist_type", "vod", 
    #     "-hls_segment_filename", segment_patter, 
    #     "-master_pl_name", master_playlist, 
    #     "-var_stream_map", "v:0,a:0 v:1,a:1", playlist_patter,
    # ]
    # print("command defined")
    # command = [
    #     "ffmpeg", "-i", str(video_data["video_dir"]),
    #     "-filter:v:0", "scale=w=1280:h=720:force_original_aspect_ratio=decrease", "-b:v:0", "3000k",
    #     "-filter:v:1", "scale=w=1920:h=1080:force_original_aspect_ratio=decrease", "-b:v:1", "6000k",
    #     "-c:v", "h264",
    # ]

    # # "-filter:v:0", "scale=w=1280:h=720", "-b:v:0", "3000k",
    # # "-filter:v:1", "scale=w=1920:h=1080", "-b:v:1", "6000k",

    # if has_audio:
    # command += ["-c:a", "aac", "-strict", "-2"]
    # command += ["-map", "0:v", "-map", "0:a", "-map", "0:v", "-map", "0:a"]
    # command += ["-var_stream_map", "v:0,a:0 v:1,a:1"]
    # print("[+] Audio")
    # else:
    #     command += ["-map", "0:v", "-map", "0:v"]
    #     command += ["-var_stream_map", "v:0 v:1"]
    #     # print("[-] Audio")

    # command += [
    #     "-f", "hls",
    #     "-hls_time", "6",
    #     "-hls_list_size", "0",
    #     "-master_pl_name", "master.m3u8",
    #     "stream_%v.m3u8"
    # ]

    command = [
        "ffmpeg", 
        "-i", str(video_data["video_dir"]),
        "-filter_complex",
        "[0:v]split=2[v1][v2];"
        "[v1]scale=w=1280:h=720:force_original_aspect_ratio=decrease,scale=trunc(iw/2)*2:trunc(ih/2)*2[v1out];"
        "[v2]scale=w=1920:h=1080:force_original_aspect_ratio=decrease,scale=trunc(iw/2)*2:trunc(ih/2)*2[v2out]",
        "-map", "[v1out]", "-b:v:0", "3000k",
        "-map", "0:a?", "-c:a:0", "aac", "-b:a:0", "128k", "-ac", "2",
        "-map", "[v2out]", "-b:v:1", "6000k", 
        "-map", "0:a?", "-c:a:1", "aac", "-b:a:1", "128k", "-ac", "2",
        "-c:v", "libx264",
        "-f", "hls",
        "-hls_time", "6",
        "-hls_list_size", "0",
        "-hls_playlist_type", "vod",
        "-master_pl_name", "master.m3u8",
        "-var_stream_map", "v:0,a:0 v:1,a:1",
        "stream_%v.m3u8"
    ]

    process = await asyncio.create_subprocess_exec(
        *command, cwd=output_dir,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if stdout:
        print("Stdout: \n", stdout.decode())
    if stderr:
        print("Stderr: \n", stderr.decode())

    await process.wait()

    if process.returncode == 0:
        print("mandando data")
        os.remove(video_data["video_dir"])
        await upload_files(video_data["video_id"], video_data["dir"])
        await delete_file(video_data["video_id"])
        shutil.rmtree(video_data["dir"])
        await post_data_api("/api/studio/video-upload-status", {
            "video_id": video_data["video_id"],
            "video_status": "ready"
        })
        print("[+] Ready")
        return True
    else:
        print("algo paso")
        return False


########## Video  ##########
async def video_converter():
    while True:

        data = await queue.get()

        result = await hls_converter(data)

        # request.post(settings.CDN_ORIGIN + "/nodes/video_status", json=data)

        queue.task_done()
