'use client';

/********************** Modules **********************/
import { useRouter } from "next/navigation";
import { use, useState, useEffect } from "react";

// DOM
import Link from "next/link";
import VideoCarousel from "@/components/actions/Video-Carousel"

// Icons
import { GiElectric } from "react-icons/gi";
import { HiFire } from "react-icons/hi2";

// Routes
import { routes } from "@/helpers/routes";

// Auth
import { useAuth } from "@/context/auth";

// Notifications
import { useNotification } from "@/context/notifications";

// Utils
import { create_params } from "@/helpers/utils";

// API
import { get_data, send_data } from "@/helpers/api";

/********************** Channel **********************/
const Channel = ({ params }: { params: Promise<{ tag: string }> }) => {
    // Notifications
    const { notify } = useNotification();

    // Auth
    const { user } = useAuth();

    // Router
    const router = useRouter();

    // Query
    let { tag } = use(params);
    tag = decodeURIComponent(tag);

    // Structure
    interface Channel {
        name: string,
        description: string,
        tag: string,
        avatar_url: string,
        user_id: string,
        date: string,
    }

    // States
    const [loading, setLoading] = useState(true);
    const [isValid, setIsValid] = useState(false);
    const [creator, setCreator] = useState(false);
    const [followers, setFollowers] = useState(0);
    const [videos, setVideos] = useState(0);

    const [channel, setChannel] = useState<Channel>({} as Channel);
    const [activeTab, setActiveTab] = useState("home");

    // Check @
    useEffect(() => {
        if (typeof tag === "string") {
            if (tag.startsWith("@")) setIsValid(true);
            else router.push(routes.public.home);
        } else router.push(routes.public.home);
    }, [tag, router]);

    const tag_txt = tag.replace("@", "");

    // Get info
    useEffect(() => {
        if (!isValid || !tag_txt) return;
        const get_channel = async () => {
            const params = create_params({
                tag: tag_txt,
            });

            // Request
            const data = await get_data(`/api/channels/get${params}`, {}, notify, true);

            if (!data) {
                window.location.href = routes.public.home;
            }

            const channel = data.channel;
            const followers = data.followers;
            const videos = data.videos;

            setVideos(videos);
            setChannel(channel);
            setFollowers(followers);

            setLoading(false);

            if (user)
                if (channel.user_id == user.id) setCreator(true);
        }

        get_channel()
    }, [isValid, tag_txt]);

    // 
    if (!isValid) {
        return null;
    }

    // DOM
    return (
        <div className="content">
            {!loading ? (
                <>
                    <div className="channel-view-info-container-p">
                        <div className="channel-view-banner-container"></div>
                        <div className="channel-view-info-container-dark"></div>
                        <div className="channel-view-info-container-content">
                            <div className="channel-view-info-content-img-container">
                                <img src={channel.avatar_url} alt="Channel logo" className="channel-view-info-content-img" />
                            </div>
                            <div className="channel-view-info-content">
                                <div className="channel-view-info-content-top">
                                    <div className="channel-view-info-content-top-left">
                                        <span className="channel-view-info-content-title">{channel.name}</span>
                                        <div className="channel-view-info-content-extra-info-container">
                                            <span className="channel-view-info-content-extra-info-text">{followers} followers</span>
                                            <span className="channel-view-info-content-extra-info-text">{videos} videos</span>
                                        </div>
                                    </div>
                                    {creator ? (
                                        <Link href={routes.studio.channels.manage_tag(tag_txt)} className="channel-view-info-content-action channel-view-info-content-action-creator">Floua Studio</Link>
                                    ) : (
                                        <Link href="#" className="channel-view-info-content-action">Follow</Link>
                                    )}
                                </div>
                                <div className="channel-view-info-content-bottom">
                                    <span className="channel-view-info-content-bottom-text">{channel.description}</span>
                                    <div className="channel-view-info-content-bottom-actions"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="channel-view-body-container">
                        <div className="channel-view-body-header">
                            <div className="channel-view-body-header-options">
                                <button className={`channel-options-btn ${activeTab == "home" ? "channel-options-btn-active" : ""}`} onClick={() => setActiveTab("home")}>
                                    Home
                                </button>
                                <button className={`channel-options-btn ${activeTab == "videos" ? "channel-options-btn-active" : ""}`} onClick={() => setActiveTab("videos")}>
                                    Videos
                                </button>
                                <button className={`channel-options-btn ${activeTab == "playlists" ? "channel-options-btn-active" : ""}`} onClick={() => setActiveTab("playlists")}>
                                    Playlists
                                </button>
                            </div>
                            <div className="">
                                <input type="text" placeholder={`Search in ${channel.name} `} />
                            </div>
                        </div>
                        <div className="channel-view-body">
                            {activeTab == "home" && (
                                <div className="channel-view-body-home-container">
                                    <VideoCarousel endpoint={`/api/videos/newest/${channel.tag}`} title="Latest Videos" icon={<GiElectric className="color-orange" size={40} />} />
                                    <VideoCarousel endpoint={`/api/videos/popular/${channel.tag}`} title="Popular Videos" icon={<HiFire className="color-salmon" size={40} />} />
                                </div>
                            )}
                        </div>
                    </div>
                </>
            ) : (
                <></>
            )}
        </div>
    );
};

export default Channel;