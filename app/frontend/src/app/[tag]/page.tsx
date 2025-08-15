'use client';

/********************** Modules **********************/
import { useRouter } from "next/navigation";
import { use, useState, useEffect } from "react";

// DOM
import Link from "next/link";

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
    const [isValid, setIsValid] = useState(false);
    const [creator, setCreator] = useState(false);
    const [followers, setFollowers] = useState(0);
    const [videos, setVideos] = useState(0);

    const [channel, setChannel] = useState<Channel>({} as Channel);

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
            const data = await get_data(`/api/channels/get${params}`, {}, notify);

            if (!data) {
                setTimeout(() => {
                    window.location.href = routes.public.home;
                }, 500);
            }

            const channel = data.channel;
            const followers = data.followers;
            const videos = data.videos;

            setChannel(channel);
            setFollowers(followers);
            setVideos(videos);

            if (user)
                if (channel.user_id == user.id) setCreator(true);
        }

        get_channel()
    }, [isValid, tag_txt, setChannel]);

    // 
    if (!isValid) {
        return null;
    }

    // DOM
    return (
        <div className="content">
            <div className="channel-view-container">
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
                                    <Link href="#" className="channel-view-info-content-action channel-view-info-content-action-creator">Edit Channel</Link>   
                                ): (
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
                <div className="">

                </div>
            </div>
        </div>
    );
};

export default Channel;