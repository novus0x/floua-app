'use client';

/********************** Modules **********************/
import { useRouter } from "next/navigation";
import { use, useState, useEffect, useRef } from "react";

import { Chart, ChartConfiguration, ChartData, ChartType, plugins, registerables } from "chart.js";

// DOM
import Link from "next/link";

// Icons
import { FaUsers, FaVideo, FaEye } from "react-icons/fa6";
import { LuWaypoints } from "react-icons/lu";
import { HiUpload } from "react-icons/hi";

// Routes
import { routes } from "@/helpers/routes";

// Auth
import { useAuth } from "@/context/auth";

// Settings
import { settings } from "@/helpers/settings";

// Notifications
import { useNotification } from "@/context/notifications";

// API
import { get_data, send_data } from "@/helpers/api";

// Utils
import { creators_only } from "@/helpers/utils";

/********************** Variables **********************/
Chart.register(...registerables);

/********************** Studio **********************/
const Manage = ({ params }: { params: Promise<{ tag: string }> }) => {
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
    interface Latest_Video {
        short_id: string,
        title: string,
        status: string,
        visibility: string,
        views: string,
        popularity: string,
        comments: string,
    }

    interface Channel {
        views: string,
        followers: string,
        points: string,
        videos: string,
        latest_videos: Latest_Video[],
    }

    // States
    const [channel, setChannel] = useState<Channel>({
        views: '0',
        followers: '0',
        points: '0',
        videos: '0',
        latest_videos: [],
    });

    // Referencies
    const canvas_ex = useRef<HTMLCanvasElement | null>(null);
    const chart_ex = useRef<Chart | null>(null);

    const canvas_ex_2 = useRef<HTMLCanvasElement | null>(null);
    const chart_ex_2 = useRef<Chart | null>(null);

    // Variables
    let check_role = false;
    let check_user_creator = false;

    // Role
    useEffect(() => {
        // 
        const get_channel_info = async () => {
            const data = await get_data(`/api/studio/manage/channels/${tag}`, {}, notify, true);

            if (!data) {
                setTimeout(() => {
                    return window.location.href = routes.studio.home
                }, 1500);
            } else {
                setChannel(data.channel)
                console.log(data);
            }
        };

        // 
        if (!check_role) {
            creators_only(user, notify, "Create your channel to start using Floua Studio");
            check_role = true;
        }

        if (!check_user_creator) {
            get_channel_info();
            check_user_creator = true;
        }

    }, [creators_only])

    // Graph
    useEffect(() => {
        if (!canvas_ex.current || !canvas_ex_2.current) return;

        const canva_ex_date: ChartData<"line"> = {
            labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
            datasets: [{
                label: "Votes",
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: "#FD420A",
                borderColor: "#FF5733",
                borderWidth: 4,
                tension: 0.4,
            }],
        };

        const canva_ex_date_2: ChartData<"pie"> = {
            labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
            datasets: [{
                label: "Votes",
                data: [12, 19, 3, 5, 2, 3],
                // backgroundColor: "#FD420A",
                // borderColor: "#FF5733",
                // borderWidth: 4,
            }],
        };

        const canva_config_ex: ChartConfiguration<"line"> = {
            type: "line",
            data: canva_ex_date,
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true },
                    title: { display: true, text: "Votes per Color" },
                },
            },
        };

        const canva_config_ex_2: ChartConfiguration<"pie"> = {
            type: "pie",
            data: canva_ex_date_2,
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true },
                    title: { display: true, text: "Votes per Color" },
                },
            },
        };

        chart_ex.current = new Chart(canvas_ex.current, canva_config_ex);
        chart_ex_2.current = new Chart(canvas_ex_2.current, canva_config_ex_2);

        return () => {
            chart_ex.current?.destroy();
            chart_ex_2.current?.destroy();
        };

    })

    // DOM
    return (
        <div className="studio-content">
            <div className="studio-content-breadcrumps-extra-container">
                <div className="studio-content-breadcrumps">
                    <Link href={routes.studio.home}>Home</Link> / <Link href={routes.studio.channels.manage}>Channel</Link> / <span className="studio-content-breadcrumps-active">{tag}</span>
                </div>
                <div>
                    <Link href={routes.studio.channels.upload_tag(tag)} className="studio-content-breadcrumps-button"><HiUpload size={18} /> Upload Video</Link>
                </div>
            </div>

            <div className="studio-content-summary">
                <div className="studio-content-summary-block">
                    <div className="studio-content-summary-block-info">
                        <div className="studio-content-summary-block-info-icon-container">
                            <div className="studio-content-summary-block-info-icon-background"></div>
                            <div className="studio-content-summary-block-info-icon">
                                <FaEye />
                            </div>
                        </div>
                        <div className="studio-content-summary-block-vals-container">
                            <span className="studio-content-summary-block-value">{channel.views}</span>
                            <span className="studio-content-summary-block-text">Views</span>
                        </div>
                    </div>
                </div>
                <div className="studio-content-summary-block">
                    <div className="studio-content-summary-block-info">
                        <div className="studio-content-summary-block-info-icon-container">
                            <div className="studio-content-summary-block-info-icon-background"></div>
                            <div className="studio-content-summary-block-info-icon">
                                <FaUsers />
                            </div>
                        </div>
                        <div className="studio-content-summary-block-vals-container">
                            <span className="studio-content-summary-block-value">{channel.followers}</span>
                            <span className="studio-content-summary-block-text">Followers</span>
                        </div>
                    </div>
                </div>
                <div className="studio-content-summary-block">
                    <div className="studio-content-summary-block-info">
                        <div className="studio-content-summary-block-info-icon-container">
                            <div className="studio-content-summary-block-info-icon-background"></div>
                            <div className="studio-content-summary-block-info-icon">
                                <LuWaypoints />
                            </div>
                        </div>
                        <div className="studio-content-summary-block-vals-container">
                            <span className="studio-content-summary-block-value">{channel.points}</span>
                            <span className="studio-content-summary-block-text">Points earned</span>
                        </div>
                    </div>
                </div>
                <div className="studio-content-summary-block">
                    <div className="studio-content-summary-block-info">
                        <div className="studio-content-summary-block-info-icon-container">
                            <div className="studio-content-summary-block-info-icon-background"></div>
                            <div className="studio-content-summary-block-info-icon">
                                <FaVideo />
                            </div>
                        </div>
                        <div className="studio-content-summary-block-vals-container">
                            <span className="studio-content-summary-block-value">{channel.videos}</span>
                            <span className="studio-content-summary-block-text">Videos</span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="studio-content-channel-canva">
                <div className="studio-content-channel-canva-left">
                    <canvas ref={canvas_ex} className="studio-content-channel-canva-left-content"></canvas>
                </div>
                <div className="studio-content-channel-canva-right">
                    <canvas ref={canvas_ex_2} className="studio-content-channel-canva-left-content"></canvas>
                </div>
            </div>

            <div className="studio-content-table-container">
                <div className="studio-content-table-header">
                    <span className="studio-content-table-header-title">Latest Videos</span>
                </div>

                <table className="studio-content-table">
                    <thead className="studio-content-table-head">
                        <tr className="studio-content-table-head-element">
                            <th className="studio-content-table-head-element-text">Title</th>
                            <th className="studio-content-table-head-element-text">Status</th>
                            <th className="studio-content-table-head-element-text">Visibility</th>
                            <th className="studio-content-table-head-element-text">Views</th>
                            <th className="studio-content-table-head-element-text">Popularity</th>
                            <th className="studio-content-table-head-element-text">Comments</th>
                            <th className="studio-content-table-head-element-text">Actions</th>
                        </tr>
                    </thead>

                    <tbody className="studio-content-table-body">
                        {channel.latest_videos.map(video => (
                            <tr className="studio-content-table-body-element" key={video.short_id}>
                                <td className="studio-content-table-body-element-text">{video.title}</td>
                                <td className="studio-content-table-body-element-text">{video.status}</td>
                                <td className="studio-content-table-body-element-text">{video.visibility}</td>
                                <td className="studio-content-table-body-element-text">{video.views}</td>
                                <td className="studio-content-table-body-element-text">{video.popularity}</td>
                                <td className="studio-content-table-body-element-text">{video.comments}</td>
                                <td className="studio-content-table-body-element-text">
                                    <Link href={` #${video.short_id} `} className="studio-content-table-body-element-text-link">Edit Video</Link>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                <div className="studio-content-table-footer">

                </div>
            </div>


        </div>
    );
};

export default Manage;