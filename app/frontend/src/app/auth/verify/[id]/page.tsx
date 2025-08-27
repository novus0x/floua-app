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

// API
import { get_data, send_data } from "@/helpers/api";

/********************** Channel **********************/
const Channel = ({ params }: { params: Promise<{ id: string }> }) => {
    // Notifications
    const { notify } = useNotification();

    // Query
    let { id } = use(params);
    id = decodeURIComponent(id);

    // Variables
    let already = false;

    useEffect(() => {
        const verify_account = async () => {
            const data = await send_data("/api/users/verify", {}, {
                id: id
            }, notify);

            setTimeout(() => {
               return window.location.href = routes.public.home; 
            }, 500);
        }

        if (!already) {
            verify_account();
            already = true;
        }

    }, [already, id]);

    // DOM
    return (
        <div className="auth-container">
            <video src="/videos/video_background.mp4" autoPlay loop muted className="auth-video-background"></video>
            <div className="auth-video-overlay"></div>

            <div className="auth-container-form">
                <div className="form-auth-container" >
                    <div className="auth-brand-full">
                        <a href={routes.public.home} className="auth-brand-full-logo-container">
                            <img src="/img/icon.svg" alt="Floua Logo" className="auth-brand-full-logo" />
                            <span className="auth-brand-full-text">Floua</span>
                            <span className="auth-brand-full-text-extra">Beta</span>
                        </a>
                    </div>

                    <span className="auth-chage-link-container">Verifying your account</span>
                    <span className="auth-chage-link-container">You will be redirected soon!</span>
                </div>

                <span className="auth-brand-full-text-small">No more instrusive ads. Just creator-powered sponsorships.</span>
            </div>
        </div>
    );
};

export default Channel;