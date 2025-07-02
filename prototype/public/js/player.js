/*** Modules ***/
import { format_time } from "./utils.js";

/*** DOM Elements ***/
const video = document.getElementById("video");
const video_container = document.getElementById("video-container");
const video_player_play = document.getElementById("video-player-play");
const video_player_volume = document.getElementById("video-player-volume");
const video_player_controls = document.getElementById("video-player-controls");
const video_player_fullscreen = document.getElementById("video-player-fullscreen");
const video_player_volume_input = document.getElementById("video-player-volume-input");
const video_player_volume_container = document.getElementById("video-player-volume-container");
const video_player_progress_container = document.getElementById("video-player-progress-container");

/*** Variables ***/
let checked = false;
let timeout_d = null;
let first_play = false;
let video_muted = false;
let last_audio_value = 50;
let active_controls = true;
let active_volume_controls = false;

/*** Preload video ***/
const hls = new Hls();
let quality = 1080;
// const video_url = `../public/videos/stream_${quality == "720" ? 0 : 1}.m3u8`;
const video_url = `../public/videos/master.m3u8`;

hls.loadSource(video_url);
hls.attachMedia(video);

/*** Functions ***/
function video_play_video_controller() {
    if (!first_play) first_play = true;
    if (video.paused || video.ended) {
        video.play();
        video_player_play.textContent = "pause";
    }
    else {
        video.pause();
        video_player_play.textContent = "play_arrow";
    }
}

function change_video_time(element) {
    const rect = video_player_progress_container.getBoundingClientRect();
    const clickX = element.clientX - rect.left;
    const moment = clickX / rect.width;

    video.currentTime = moment * video.duration;
}

function full_screen() {
    if (!document.fullscreenElement) video_container.requestFullscreen();
    else document.exitFullscreen();
}

function show_controls() {
    if (active_controls) return 0;
    active_controls = true;
    video_player_controls.classList.add("fade-in");
    video_player_controls.classList.remove("hidden");
}

function hide_controls() {
    clearTimeout(timeout_d);
    timeout_d = setTimeout(() => {
        video_player_controls.classList.add("fade-out");
        setTimeout(() => {
            active_controls = false;
            video_player_controls.classList.add("hidden");
            video_player_controls.classList.remove("fade-out");
        }, 1000)
    }, 2500);
}

function toggle_controls() {
    if (!first_play) return 0;

    if (active_controls) hide_controls();
    else show_controls();
}

function volume_icon() {
    if (video.volume == 0) video_player_volume.textContent = "volume_off";
    else if (video.volume <= 0.5) video_player_volume.textContent = "volume_down";
    else video_player_volume.textContent = "volume_up";
}

function toggle_volume() {
    if (video_muted) {
        video_muted = false;
        video.volume = last_audio_value / 100;
    } else {
        video.volume = 0;
        video_muted = true;
    }
    volume_icon();
}

function change_volume() {
    last_audio_value = video_player_volume_input.value;
    video.volume = video_player_volume_input.value / 100;
    volume_icon();
}

function show_volume_controller() {
    if (active_volume_controls) return 0;
    active_volume_controls = true;
    video_player_volume_input.classList.remove("hidden");
    video_player_volume_input.classList.add("scale-in-hor-left");
}

function hide_volume_controller() {
    if (!active_volume_controls) return 0;
    if (!video_player_volume_input.classList.contains("scale-out-hor-left")) {
        video_player_volume_input.classList.add("scale-out-hor-left");
        video_player_volume_input.classList.remove("scale-in-hor-left");
    }
    setTimeout(() => {
        active_volume_controls = false;
        video_player_volume_input.classList.add("hidden");
        video_player_volume_input.classList.remove("scale-out-hor-left");
    }, 500);
}

/*** Events ***/
video_container.addEventListener("mousemove", toggle_controls);
video_container.addEventListener("touchstart", toggle_controls);

video.addEventListener("loadedmetadata", () => {
    video.currentTime = 0.1
    volume_icon();
});
video.addEventListener("click", video_play_video_controller);
video.addEventListener("timeupdate", () => {
    const video_player_current_time = document.getElementById("video-player-time-current");
    const video_player_total_time = document.getElementById("video-player-time-total");
    const video_player_progress = document.getElementById("video-player-progress");

    const seconds_now = video.currentTime;
    const seconds_total = video.duration;

    const current_time = format_time(seconds_now);
    const total_time = format_time(seconds_total || 0);

    video_player_current_time.textContent = current_time;
    video_player_total_time.textContent = total_time;

    const progress_value = seconds_now / seconds_total;
    video_player_progress.style.width = `${100 * progress_value}%`;

    // Especial action (0.90)
    if (progress_value > 0.90 && !checked) {
        console.log("Watched");
        checked = true;
    }
})

// Progress bar
video_player_progress_container.addEventListener("click", change_video_time);

// Play
video_player_play.addEventListener("click", video_play_video_controller);

// Volume
video_player_volume.addEventListener("click", toggle_volume);
video_player_volume_container.addEventListener("mousemove", show_volume_controller);
video_player_volume_container.addEventListener("mouseleave", hide_volume_controller);

video_player_volume_input.addEventListener("input", (e) => change_volume(e.target));

// Full Screen
video_player_fullscreen.addEventListener("click", full_screen);

// Keyboard Shortcuts (soon)
// document.addEventListener("keydown", (e) => {
//     if (e.key == "Escape" || e.key == "Esc") {
//         if (document.fullscreenElement) full_screen();
//     } else if (e.key == "f") {
//         full_screen();
//     }
// });

