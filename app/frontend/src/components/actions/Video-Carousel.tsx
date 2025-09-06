'use client';

/********************** Modules **********************/
import { useRouter } from "next/navigation";
import { useState, useEffect, useRef } from "react";

// DOM
import Link from "next/link";

// Icons
import { MdKeyboardArrowRight, MdKeyboardArrowLeft } from "react-icons/md";

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
    icon: React.ReactElement,
    actions?: boolean,
    text?: string,
    url?: string,
}

/********************** Home **********************/
const VideoCarousel = ({ endpoint, title, icon, actions = false, text = "", url = "#" }: VideoCarouselProps) => {
    // Router
    const router = useRouter();

    // Structures
    interface Video {
        short_id: string,
        title: string,
        views: string,
        thumbnail_url: string,

        channel_name: string,
        channel_tag: string,
        channel_avatar: string,
    }

    // States
    const [videos, setVideos] = useState<Video[]>([]);
    const [showLeftButton, setShowLeftButton] = useState(false);
    const [showRightButton, setShowRightButton] = useState(false);

    // Refs
    const carouselRef = useRef<HTMLDivElement>(null);

    // Variables
    let call_video = false;

    const checkScrollPosition = () => {
        if (carouselRef.current) {
            const { scrollLeft, scrollWidth, clientWidth } = carouselRef.current;
            setShowLeftButton(scrollLeft > 0);
            setShowRightButton(scrollLeft < scrollWidth - clientWidth - 10);
        }
    };

    const scrollLeft = () => {
        if (carouselRef.current) {
            carouselRef.current.scrollBy({ left: -340, behavior: 'smooth' });
        }
    };

    const scrollRight = () => {
        if (carouselRef.current) {
            carouselRef.current.scrollBy({ left: 340, behavior: 'smooth' });
        }
    };

    // Call API
    useEffect(() => {
        if (call_video) return;

        const get_videos = async () => {
            let data = await get_data(endpoint, {});
            setVideos(data.videos)
        }

        get_videos()
        call_video = true;
    }, [])

    useEffect(() => {
        checkScrollPosition();
        window.addEventListener('resize', checkScrollPosition);

        return () => {
            window.removeEventListener('resize', checkScrollPosition);
        };
    }, [videos]);

    return (
        <div className="floua-video-carousel-container">
            <div className="floua-video-carousel-header">
                <div className="floua-video-carousel-header-title">
                    {icon}
                    <span className="floua-video-carousel-header-title-text">{title}</span>
                </div>
                {actions ? (
                    <Link href={url} className="floua-video-carousel-header-actions">
                        <span className="floua-video-carousel-header-actions-text">{text}</span>
                        <MdKeyboardArrowRight size={30} />
                    </Link>
                ) : (
                    <></>
                )}
            </div>

            <div className="floua-video-carousel-wrapper">
                {showLeftButton && (
                    <button
                        className="floua-video-carousel-button floua-video-carousel-button-left"
                        onClick={scrollLeft}
                        aria-label="Scroll left"
                    >
                        <MdKeyboardArrowLeft size={30} />
                    </button>
                )}

                <div
                    className="floua-video-carousel-body"
                    ref={carouselRef}
                    onScroll={checkScrollPosition}
                >
                    {videos.map(video => (
                        <div className="floua-video-carousel-item-container" key={video.short_id}>
                            <Link href={routes.public.watch(video.short_id)} className="floua-video-carousel-item-video-container">
                                <img src={video.thumbnail_url} alt="Video thumbnail" className="floua-video-carousel-item-video-container-img" />
                            </Link>
                            <div className="floua-video-carousel-item-info-container">
                                <Link href={routes.channel.home(video.channel_tag)} className="floua-video-carousel-item-info-channel-avatar">
                                    <img src={video.channel_avatar} alt="Channel avatar" />
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

                {showRightButton && (
                    <button
                        className="floua-video-carousel-button floua-video-carousel-button-right"
                        onClick={scrollRight}
                        aria-label="Scroll right"
                    >
                        <MdKeyboardArrowRight size={30} />
                    </button>
                )}
            </div>
        </div>
    );
};

export default VideoCarousel;