"use client";

/********************** Modules **********************/
import Hls from "hls.js";

import { useEffect, useRef, useState } from "react";

// Icons
import { BsPlay, BsPause } from "react-icons/bs";
import { MdKeyboardDoubleArrowRight } from "react-icons/md";
import { LuVolume2, LuVolume1, LuVolumeX, LuSettings, LuMaximize } from "react-icons/lu";

// Utils
import { get_cookie, set_cookie } from "@/helpers/utils";

// Structures
interface PlayerProps {
    videoSrc: string;
    autoPlay?: boolean;
    preview?: boolean;
}

// Functions
function formatTime(seconds: number): string {
    if (isNaN(seconds)) return "00:00";
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${String(minutes).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
}

function getVideoType(src: string): string {
    console.log(src)
    if (src.includes(".m3u8")) return "application/x-mpegURL";
    if (src.includes(".mpd")) return "application/dash+xml";
    if (src.includes(".mp4")) return "video/mp4";
    if (src.includes(".webm")) return "video/webm";
    return "video/mp4";
}

/********************** Video Player **********************/
const Player = ({ videoSrc, autoPlay = false, preview = false }: PlayerProps) => {
    // States
    const [isPlaying, setIsPlaying] = useState(autoPlay);
    const [volume, setVolume] = useState(0);
    const [muted, setMuted] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);
    const [showControls, setShowControls] = useState(true);
    const [showSlider, setShowSlider] = useState(false);

    // References
    const videoRef = useRef<HTMLVideoElement>(null);
    const progressRef = useRef<HTMLInputElement>(null);
    const hideTimeout = useRef<NodeJS.Timeout | null>(null);

    // HLS for .m3u8
    useEffect(() => {
        if (videoRef.current) {
            if (getVideoType(videoSrc) === "application/x-mpegURL" && Hls.isSupported()) {
                const hls = new Hls();
                hls.loadSource(videoSrc);
                hls.attachMedia(videoRef.current);
            } else {
                videoRef.current.src = videoSrc;
            }
        }
    }, [videoSrc]);

    // Handle video
    useEffect(() => {
        const video = videoRef.current;
        if (!video) return;

        const time_update = () => setCurrentTime(video.currentTime);
        const loaded_meta = () => setDuration(video.duration);

        video.addEventListener("timeupdate", time_update);
        video.addEventListener("loadedmetadata", loaded_meta);

        return () => {
            video.removeEventListener("timeupdate", time_update);
            video.removeEventListener("loadedmetadata", loaded_meta);
        };
    }, []);

    const togglePlay = () => {
        const video = videoRef.current;
        if (!video) return;

        if (video.paused || video.ended) {
            video.play();
            setIsPlaying(true);
        } else {
            video.pause();
            setIsPlaying(false);
        }
    };

    const handleProgress = (e: React.ChangeEvent<HTMLInputElement>) => {
        const video = videoRef.current;
        if (!video) return;

        const new_time = (parseFloat(e.target.value) / 100) * duration;
        video.currentTime = new_time;
        setCurrentTime(new_time);
    };

    const toggleMute = () => {
        if (videoRef.current) {
            const new_muted = !muted;
            videoRef.current.muted = new_muted;
            setMuted(new_muted);
            if (!new_muted && volume === 0) {
                videoRef.current.volume = 0.5;
                setVolume(50);
            }
        }
    };

    const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const new_volume = Number(e.target.value);
        if (videoRef.current) {
            videoRef.current.volume = new_volume / 100;
            set_cookie("user_preferences_volume", String(videoRef.current.volume * 100));
            setVolume(new_volume);
            setMuted(new_volume === 0);
        }
    };

    const toggleFullScreen = () => {
        if (!document.fullscreenElement) {
            videoRef.current?.parentElement?.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    };

    // Variables
    let volume_preference = false;

    // User preferences - volume
    useEffect(() => {
        if (volume_preference) return;
        volume_preference = true;

        const saved_volume = get_cookie("user_preferences_volume");
        if (saved_volume) {
            const v = parseInt(saved_volume, 10);
            if (videoRef.current) {
                videoRef.current.volume = v / 100;
                setVolume(v);
            }
        } else {
            set_cookie("user_preferences_volume", "100"); // default 100%
        }

    }, []);

    // Auto hide controls after inactivity
    useEffect(() => {
        let timeout: NodeJS.Timeout;
        if (showControls) {
            timeout = setTimeout(() => setShowControls(false), 3000);
        }
        return () => clearTimeout(timeout);
    }, [showControls, currentTime, isPlaying]);

    const handleMouseMove = () => {
        setShowControls(true);

        if (hideTimeout.current) clearTimeout(hideTimeout.current);

        hideTimeout.current = setTimeout(() => {
            setShowControls(false);
        }, 1500);
    };

    // DOM
    return (
        <div className="floua-player" onMouseMove={handleMouseMove} onTouchStart={handleMouseMove}>
            <video key={videoSrc} ref={videoRef} playsInline autoPlay={autoPlay} >
                <source src={videoSrc} />
            </video>

            <div className="floua-player-overlay" onClick={togglePlay}></div>

            <div className={`floua-player-controls duration-500 ${showControls ? "fade-in" : "fade-out"}`} >
                <input type="range" ref={progressRef} value={duration ? (currentTime / duration) * 100 : 0} onChange={handleProgress} className="floua-player-progress-container"
                    style={{
                        background: `linear-gradient(to right, #FD420A ${(currentTime / duration) * 100}%, #10151C ${(currentTime / duration) * 100}%)`,
                    }}
                />


                <div className="floua-player-controls-left">
                    <button onClick={togglePlay}>
                        {isPlaying ? (
                            <BsPause size={23} className="color-main floua-player-controls-icon" />
                        ) : (
                            <BsPlay size={23} className="color-main floua-player-controls-icon" />
                        )}
                    </button>

                    {!preview ? (
                        <MdKeyboardDoubleArrowRight size={23} className="color-main floua-player-controls-icon" />
                    ) : (
                        <></>
                    )}
                    <div className="floua-player-progress-volume-container">
                        <button
                            onClick={toggleMute}
                            onMouseEnter={() => setShowSlider(true)}
                        >
                            {muted || volume === 0 ? (
                                <LuVolumeX size={19} className="color-main floua-player-controls-icon" />
                            ) : volume < 50 ? (
                                <LuVolume1 size={19} className="color-main floua-player-controls-icon" />
                            ) : (
                                <LuVolume2 size={19} className="color-main floua-player-controls-icon" />
                            )}
                        </button>

                        {showSlider && (
                            <input
                                type="range"
                                min="0"
                                max="100"
                                value={volume}
                                onChange={handleVolumeChange}
                                onMouseLeave={() => setShowSlider(false)}
                                className="floua-player-progress-volume"
                            />
                        )}
                    </div>

                    <span className="color-main text-sm">
                        {formatTime(currentTime)} / {formatTime(duration)}
                    </span>
                </div>

                <div className="floua-player-controls-right">
                    {!preview ? (
                        <LuSettings size={20} className="color-main floua-player-controls-icon" />
                    ) : (
                        <></>
                    )}
                    <button onClick={toggleFullScreen}>
                        <LuMaximize size={20} className="color-main floua-player-controls-icon" />
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Player;
