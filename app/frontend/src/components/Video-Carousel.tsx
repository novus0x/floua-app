'use client';

/********************** Modules **********************/
import { useRouter } from "next/navigation";
import { use, useState, useEffect } from "react";

// DOM
import Link from "next/link";

// Icons
import { MdKeyboardArrowRight } from "react-icons/md";

// Auth
import { useAuth } from "@/context/auth";

// Routes
import { routes } from "@/helpers/routes";

// Notifications
import { useNotification } from "@/context/notifications";

// API
import { get_data } from "@/helpers/api";

// Structure
interface VideoCarouselProps {
    endpoint: string,
    title: string,
    icon: React.ReactElement
}

/********************** Home **********************/
const VideoCarousel = ({ endpoint, title, icon }: VideoCarouselProps) => {
    // Router
    const router = useRouter();

    // Structures
    interface Video {
        short_id: string,
        title: string,
        views: string,

        channel_name: string,
        channel_tag: string,
        channel_avatar: string,
    }

    // States
    const [videos, setVideos] = useState<Video[]>([]);

    // Variables
    let call_video = false;

    // Call API
    useEffect(() => {
        if (call_video) return;

        const get_videos = async () => {
            let data = await get_data(endpoint, {});
            setVideos(data.videos)
            console.log(data.videos)
        }

        get_videos()
        call_video = true;
    }, [])


    return (
        <div className="floua-video-carousel-container">
            <div className="floua-video-carousel-header">
                <div className="floua-video-carousel-header-title">
                    {icon}
                    <span className="floua-video-carousel-header-title-text">{title}</span>
                </div>
                <Link href="#watch-more" className="floua-video-carousel-header-actions">
                    <span className="floua-video-carousel-header-actions-text">Watch more</span>
                    <MdKeyboardArrowRight size={30} />
                </Link>
            </div>
            <div className="floua-video-carousel-body">
                {videos.map(video => (
                    <div className="floua-video-carousel-item-container" key={video.short_id}>
                        <Link href={routes.public.watch(video.short_id)} className="floua-video-carousel-item-video-container">
                            {/* <img src="" alt="" /> */}
                        </Link>
                        <div className="floua-video-carousel-item-info-container">
                            <Link href={routes.channel.home(video.channel_tag)} className="floua-video-carousel-item-info-channel-avatar">
                                <img src={video.channel_avatar} alt="" />
                            </Link>
                            <div className="floua-video-carousel-item-info">
                                <Link href={routes.public.watch(video.short_id)} className="floua-video-carousel-item-info-title">{video.title}</Link>
                                <div className="floua-video-carousel-item-info-extra">
                                    <Link href={routes.channel.home(video.channel_tag)}>{video.channel_name}</Link>
                                    <span>{video.views} views</span>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default VideoCarousel;