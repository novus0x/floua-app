'use client';

/********************** Modules **********************/
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

// DOM
import Link from "next/link";
import Player from "@/components/actions/Player";
import Comments from "@/components/actions/Comments";
import VideoSuggestionList from "@/components/actions/Video-Suggestion-List";

// Icons
import { GoVideo } from "react-icons/go";
import { FaRegComment, FaHeart, FaHeartBroken } from "react-icons/fa";
import { FaInstagram, FaXTwitter, FaDiscord, FaGithub, FaLink } from "react-icons/fa6";

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
  const [currentTab, SetCurrentTab] = useState("videos");

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
                  <div className="floua-watch-content-extra-container-selection">
                    <button className={`floua-watch-content-extra-container-selection-btn ${currentTab == "videos" ? "floua-watch-content-extra-container-selection-btn-active" : ""} `} onClick={() => SetCurrentTab("videos")}>Videos</button>
                    <button className={`floua-watch-content-extra-container-selection-btn ${currentTab == "comments" ? "floua-watch-content-extra-container-selection-btn-active" : ""} `} onClick={() => SetCurrentTab("comments")}>Comments</button>
                  </div>
                  <div className={`${currentTab == "comments" ? "" : "floua-watch-content-extra-container-selection-hidden"} `}>
                    <div className="floua-watch-content-subtitle-container">
                      <FaRegComment className="color-main" size={32} />
                      <span className="floua-watch-content-subtitle-text">Comments</span>
                    </div>
                    <div>
                      <Comments />
                    </div>
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
                  <div className="floua-watch-content-extra-container-info">
                    <div className="floua-watch-content-extra-container-info-video">
                      <span>Views</span>
                      <span>Time</span>
                    </div>
                    <div className="floua-watch-content-extra-container-info-social">
                      <a href="#" target="_blank"><FaInstagram className="color-main" size={25} /></a>
                      <a href="#" target="_blank"><FaXTwitter className="color-main" size={25} /></a>
                      <a href="#" target="_blank"><FaDiscord className="color-main" size={25} /></a>
                      <a href="#" target="_blank"><FaGithub className="color-main" size={25} /></a>
                      <a href="#" target="_blank"><FaLink className="color-main" size={25} /></a>
                    </div>
                    <div className="floua-watch-content-extra-container-info-tags">
                      <a href="#" className="floua-watch-content-extra-tag">#Tag</a>
                      <a href="#" className="floua-watch-content-extra-tag">#Tag</a>
                      <a href="#" className="floua-watch-content-extra-tag">#Tag</a>
                      <a href="#" className="floua-watch-content-extra-tag">#Tag</a>
                      <a href="#" className="floua-watch-content-extra-tag">#Tag</a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className={`floua-watch-right ${currentTab == "videos" ? "" : "floua-watch-content-extra-container-selection-hidden"} `}>
            <div className="floua-watch-content-subtitle-container">
              <GoVideo className="color-main" size={32} />
              <span className="floua-watch-content-subtitle-text">You might like</span>
            </div>
            <div>
              <VideoSuggestionList />
            </div>
          </div>
        </div>
      ) : (
        <></>
      )}

    </div>
  );
};

export default Watch;