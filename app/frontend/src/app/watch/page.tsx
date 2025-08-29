'use client';

/********************** Modules **********************/
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

// DOM
import Link from "next/link";
import Player from "@/components/Player";

// Icons
import { FaComment, FaHeart, FaHeartBroken } from "react-icons/fa";

// Auth
import { useAuth } from "@/context/auth";

// Notifications
import { useNotification } from "@/context/notifications";

// Routes
import { routes } from "@/helpers/routes";

// API
import { get_data, send_data, send_files } from "@/helpers/api";

/********************** Trending **********************/
const Watch = () => {
  // Notifications
  const { notify } = useNotification();

  // Auth
  const { user } = useAuth();

  // Router
  const router = useRouter();

  // Video ID
  const search_params = useSearchParams();
  const id = search_params.get("id");

  // Structure
  interface Video {
    short_id: string,
    title: string,
    status: string,
    description: string,

    views: string,
    likes: string,
    dislikes: string,

    date: string
  }

  interface Channel {
    tag: string,
    name: string,
    avatar: string,
    followers: string,
  }

  // States
  const [videoLoaded, setVideoLoaded] = useState(false);
  const [videoSource, setVideoSource] = useState("");
  const [video, setVideo] = useState<Video>({
    short_id: "",
    title: "",
    status: "",
    description: "",

    views: "",
    likes: "",
    dislikes: "",

    date: ""
  });
  const [channel, SetChannel] = useState<Channel>({
    tag: "",
    name: "",
    avatar: "",
    followers: "",
  })

  // Variables
  let video_request = false;

  // 
  useEffect(() => {
    // Get Video
    if (video_request) return;
    const get_video = async () => {
      const data = await get_data(`/api/videos/watch/${id}`, {});

      if (data?.video_source) {
        setVideoSource(data.video_source);
        setVideoLoaded(true);
      } else {
        window.location.href = routes.public.home;
      }
      if (data?.video) setVideo(data.video);
      if (data?.channel) SetChannel(data.channel);
    };

    if (!video_request) {
      get_video()
      video_request = true;

    }
  }, [])

  return (
    <div className="content">

      {videoLoaded ? (
        <div className="floua-watch-container">
          <div className="floua-watch-left">
            <div className="floua-watch-player">
              {videoLoaded && videoSource ? (
                <Player key={videoSource} videoSrc={videoSource} autoPlay />
              ) : <></>}
            </div>
            <div className="floua-watch-content">
              <div className="floua-watch-title-container">
                <span className="floua-watch-title">{video.title}</span>
                <div className="floua-watch-actions-likes">
                  <button className="floua-watch-actions-likes-btn">
                    <FaHeart size={25} />
                    <span>{video.likes}</span>
                  </button>
                  <button className="floua-watch-actions-likes-btn">
                    <FaHeartBroken size={25} />
                    <span>{video.dislikes}</span>
                  </button>
                </div>
              </div>

              <div className="floua-watch-content-extra-container">
                <div className="floua-watch-content-extra-container-left">
                  <p className="floua-watch-content-description">{video.description}</p>
                  <div className="floua-watch-content-subtitle-container">
                    <FaComment className="color-main" size={32} />
                    <span className="floua-watch-content-subtitle-text">Comments</span>
                  </div>
                  <div>
                    To Do
                  </div>
                </div>

                <div className="floua-watch-content-extra-container-right">
                  <div className="floua-watch-content-extra-container-actions">
                    <div className="floua-watch-content-channel">
                      <Link href={routes.channel.home(channel.tag)} className="floua-watch-content-channel-avatar-container">
                        <img src={channel.avatar} alt="Channel Avatar" />
                      </Link>
                      <div className="floua-watch-content-channel-info">
                        <Link href={routes.channel.home(channel.tag)} className="floua-watch-content-channel-name">{channel.name}</Link>
                        <span className="floua-watch-content-channel-followers">{channel.followers} followers</span>
                      </div>
                    </div>
                    <div className="floua-watch-content-extra-actions-btns-container">
                      <button className="floua-watch-action-btn floua-watch-action-btn-follow">Follow</button>
                      <button className="floua-watch-action-btn floua-watch-action-btn-donate">Donate</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="floua-watch-right">
            <p>To Do</p>
          </div>
        </div>
      ) : (
        <></>
      )}

    </div>
  );
};

export default Watch;