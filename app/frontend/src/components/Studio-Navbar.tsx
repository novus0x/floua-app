'use client';

/********************** Modules **********************/
import { useState, useEffect, useRef } from "react";
import { usePathname } from "next/navigation";

// Icons
import { MdOutlineClose } from "react-icons/md";
import { FaBars } from "react-icons/fa";

// DOM
import Link from "next/link";

// Routes
import { routes } from "@/helpers/routes";

// UI
import { use_UI } from "@/context/ui";

// Auth
import { useAuth } from "@/context/auth";

/********************** Show **********************/
const show_navbar_paths = [
    routes.studio.home,
];

/********************** Component **********************/
const Studio_Navbar = () => {
    // States
    const { studioSidebarOpen, toggleStudioSidebar } = use_UI();

    // Ref
    const menu_ref = useRef<HTMLDivElement>(null);
    const notify_ref = useRef<HTMLDivElement>(null);

    // Auth
    const { user } = useAuth();

    // Check if valid path
    const pathname = usePathname();
    let valid = false;
    if (show_navbar_paths.some(path => pathname.startsWith(path))) valid = true;
    if (!valid) return "";

    // DOM
    return (
        <div>
            <button className="studio-sidebar-btn" onClick={toggleStudioSidebar}>
                {studioSidebarOpen ? (
                    <FaBars className="color-white" size={30} />
                ) : (
                    <MdOutlineClose className="color-white" size={30} />
                )}
            </button>
            <div className={` studio-sidebar-background ${studioSidebarOpen ? "hidden" : ""} `} onClick={toggleStudioSidebar}></div>
        </div>
    );
};

/********************** Export **********************/
export default Studio_Navbar;
