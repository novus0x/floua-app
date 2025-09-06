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

/********************** Home **********************/
const Comments = () => {
    // Router
    const router = useRouter();

    return (
        <div>
            <h1>Comments</h1>
        </div>
    );
};

export default Comments;