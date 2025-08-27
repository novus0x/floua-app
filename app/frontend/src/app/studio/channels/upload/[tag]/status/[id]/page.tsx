'use client';

/********************** Modules **********************/
import React, { useRef } from "react";
import { useRouter } from "next/navigation";
import { use, useState, useEffect } from "react";

// DOM
import Link from "next/link";
import Player from "@/components/Player";

// Icons

// Routes
import { routes } from "@/helpers/routes";

// Auth
import { useAuth } from "@/context/auth";

// Settings
import { settings } from "@/helpers/settings";

// Notifications
import { useNotification } from "@/context/notifications";

// API
import { get_data, send_data, send_files } from "@/helpers/api";

// Utils
import { creators_only } from "@/helpers/utils";

/********************** Upload **********************/
const Upload_Status = ({ params }: { params: Promise<{ tag: string, id: string }> }) => {
    // Notifications
    const { notify } = useNotification();

    // Auth
    const { user } = useAuth();

    // Router
    const router = useRouter();

    // Query
    let { tag, id } = use(params);
    tag = decodeURIComponent(tag);
    id = decodeURIComponent(id);

    // Structure

    // States

    // Reference

    // Variables
    let check_role = false;

    // Role
    useEffect(() => {
        // 
        if (!check_role) {
            creators_only(user, notify, "Create your channel to start using Floua Studio");
            check_role = true;
        }
    }, [creators_only]);

    // Functions

    // DOM
    return (
        <div className="studio-content">
            <div className="studio-content-breadcrumps-extra-container">
                <div className="studio-content-breadcrumps">
                    <Link href={routes.studio.home}>Home</Link> / <Link href={routes.studio.channels.manage}>Channel</Link> / <Link href={routes.studio.channels.manage_tag(tag)}>{tag}</Link> / <Link href={routes.studio.channels.upload_tag(tag)}>Upload</Link> / <span className="studio-content-breadcrumps-active">Status</span>
                </div>
                <div>

                </div>
            </div>

        </div>
    );
};

export default Upload_Status;