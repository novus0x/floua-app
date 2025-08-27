import os
import re
from tinytag import TinyTag
from pymediainfo import MediaInfo
import ffmpeg

def is_mobile_video(video_path: str) -> bool:
    """
    Detecta si un video fue grabado con un dispositivo móvil
    Args:
        video_path: Ruta completa al archivo de video
    Returns:
        bool: True si es video de celular, False si no
    """
    if not os.path.exists(video_path):
        return False
    
    mobile_indicators = 0
    detection_threshold = 3  # Mínimo de indicadores para considerar móvil
    
    # 1. Detección con TinyTag
    print("Tinytag")
    try:
        tag = TinyTag.get(video_path)
        metadata = tag.__dict__
        
        mobile_patterns = [
            'android', 'iphone', 'samsung', 'xiaomi', 'huawei',
            'motorola', 'lg', 'sony', 'nokia', 'google', 
            'oneplus', 'realme', 'oppo', 'vivo'
        ]
        
        print("starting 1")
        for value in metadata.values():
            if value and isinstance(value, str):
                lower_value = value.lower()
                if any(pattern in lower_value for pattern in mobile_patterns):
                    mobile_indicators += 2
                    break
    except:
        pass
    
    # Si ya alcanzamos el threshold, retornar early
    if mobile_indicators >= detection_threshold:
        return True
    
    # 2. Detección con pymediainfo
    print("Pymediainfo")
    try:
        media_info = MediaInfo.parse(video_path)
        
        for track in media_info.tracks:
            track_type = track.track_type
            
            if track_type == "General":
                for attr_name in ['commercial_name', 'format', 'writing_application', 
                                'title', 'comment', 'performer']:
                    value = getattr(track, attr_name, None)
                    if value and isinstance(value, str):
                        lower_value = value.lower()
                        if any(brand in lower_value for brand in [
                            'android', 'iphone', 'samsung', 'xiaomi', 'huawei'
                        ]):
                            mobile_indicators += 2
                        
                        if re.search(r'[A-Z]{1,2}[0-9]{3,}[A-Z]{0,2}', value) or \
                           re.search(r'iphone\d+', value.lower()):
                            mobile_indicators += 1
            
            elif track_type == "Video":
                width = getattr(track, 'width', 0)
                height = getattr(track, 'height', 0)
                
                if width and height:
                    try:
                        width = int(width)
                        height = int(height)
                        
                        # Resoluciones móviles típicas
                        mobile_resolutions = [
                            (1080, 1920), (1440, 2560), (720, 1280),
                            (1920, 1080), (2560, 1440), (1280, 720),
                            (2160, 3840), (3840, 2160)
                        ]
                        
                        if (width, height) in mobile_resolutions:
                            mobile_indicators += 1
                    except (ValueError, TypeError):
                        pass
                
                # Codecs móviles típicos
                codec = getattr(track, 'format', '').lower()
                if any(mobile_codec in codec for mobile_codec in [
                    'hevc', 'h265', 'avc', 'h264', 'mp4v'
                ]):
                    mobile_indicators += 1
                    
        if mobile_indicators >= detection_threshold:
            return True
    except:
        pass
    
    # 3. Detección con FFmpeg
    print("ffmeg")
    try:
        probe = ffmpeg.probe(video_path)
        
        # Analizar format tags
        format_tags = probe.get('format', {}).get('tags', {})
        for value in format_tags.values():
            if value and isinstance(value, str):
                lower_value = value.lower()
                if any(brand in lower_value for brand in [
                    'android', 'iphone', 'samsung', 'xiaomi', 'huawei'
                ]):
                    mobile_indicators += 2
                
                if re.search(r'[A-Z]{1,2}[0-9]{3,}[A-Z]{0,2}', value.upper()):
                    mobile_indicators += 1
        
        # Analizar streams
        for stream in probe.get('streams', []):
            if stream.get('codec_type') == 'video':
                # Verificar rotación (común en móviles)
                side_data = stream.get('side_data', [])
                for data in side_data:
                    if data.get('rotation'):
                        rotation = float(data['rotation'])
                        if abs(rotation) in [90, 270]:
                            mobile_indicators += 1
                            break
                
                # Bitrate típico móvil
                bit_rate = int(stream.get('bit_rate', 0))
                if 2000000 <= bit_rate <= 20000000:
                    mobile_indicators += 1
                    
    except:
        pass

    print(mobile_indicators >= detection_threshold)
    return mobile_indicators >= detection_threshold