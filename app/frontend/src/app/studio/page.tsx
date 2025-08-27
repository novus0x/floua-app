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

// Utils
import { creators_only } from "@/helpers/utils";

/********************** Studio **********************/
const Studio = () => {
    // Notifications
    const { notify } = useNotification();

    // Auth
    const { user } = useAuth();

    // Router
    const router = useRouter();

    // Variables
    let check_role = false;

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
            <div className="studio-content-title-container">
                <span className="studio-content-title">Hi {user.username}!</span>
            </div>




        </div>
    );
};

export default Studio;