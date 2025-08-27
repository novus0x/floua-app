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

// Settings
import { settings } from "@/helpers/settings";

// Notifications
import { useNotification } from "@/context/notifications";

// API
import { get_data, send_data } from "@/helpers/api";

// Utils
import { creators_only } from "@/helpers/utils";

/********************** Studio **********************/
const Manage = () => {
    // Notifications
    const { notify } = useNotification();

    // Auth
    const { user } = useAuth();

    // Router
    const router = useRouter();

    // Structure
    interface Channel {
        id: string,

        name: string,
        tag: string,
        followers: string,

        date: string
    }

    // States
    const [channels, setChannels] = useState<Channel[]>([]);

    // Variables
    let request_check = false;
    let check_role = false;

    // API
    useEffect(() => {
        const request_channels = async () => {
            // Variables
            let i, created, channel, channels = [];

            const data = await get_data("/api/studio/manage/channels", {});

            for (i = 0; i < data.channels.length; i++) {
                channel = data.channels[i];

                // Format date
                created = new Date(channel.date).toLocaleDateString("en-US", {
                    timeZone: settings.timeZone,
                    day: "2-digit",
                    month: "2-digit",
                    year: "2-digit",
                })

                // Add
                channels.push({
                    id: channel.id,
                    name: channel.name,
                    tag: channel.tag,
                    followers: channel.followers,
                    date: created
                })
            }

            setChannels(channels);

        };

        if (!request_check) {
            request_channels()
            request_check = true;
        }

    }, [request_check]);

    // Role
    useEffect(() => {
        if (!check_role) {
            creators_only(user, notify, "Create your channel to start using Floua Studio");
            check_role = true;
        }
    }, [creators_only])

    // DOM
    return (
        <div className="studio-content">
            <div className="studio-content-breadcrumps-extra-container">
                <div className="studio-content-breadcrumps">
                    <Link href={routes.studio.home}>Home</Link> / <span className="studio-content-breadcrumps-active">Channels - Manage</span>
                </div>
                <div>
                </div>
            </div>

            <div className="studio-content-title-container">
                <span className="studio-content-title">Manage Channels</span>
            </div>

            <div className="studio-content-table-container">
                <div className="studio-content-table-header">
                    <span className="studio-content-table-header-title">Channels</span>
                    <div className="studio-content-table-header-extra">
                        <input type="text" className="studio-content-table-header-extra-search" placeholder="Search..." />
                    </div>
                </div>

                <table className="studio-content-table">
                    <thead className="studio-content-table-head">
                        <tr className="studio-content-table-head-element">
                            <th className="studio-content-table-head-element-text">Tag</th>
                            <th className="studio-content-table-head-element-text">Name</th>
                            <th className="studio-content-table-head-element-text">Followers</th>
                            <th className="studio-content-table-head-element-text">Created</th>
                            <th className="studio-content-table-head-element-text">Actions</th>
                        </tr>
                    </thead>

                    <tbody className="studio-content-table-body">
                        {channels.map(channel => (
                            <tr className="studio-content-table-body-element" key={channel.id}>
                                <td className="studio-content-table-body-element-text">{channel.tag}</td>
                                <td className="studio-content-table-body-element-text">{channel.name}</td>
                                <td className="studio-content-table-body-element-text">{channel.followers}</td>
                                <td className="studio-content-table-body-element-text">{channel.date}</td>
                                <td className="studio-content-table-body-element-text">
                                    <Link href={routes.studio.channels.manage_tag(channel.tag)} className="studio-content-table-body-element-text-link">Go to my Channel</Link>
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