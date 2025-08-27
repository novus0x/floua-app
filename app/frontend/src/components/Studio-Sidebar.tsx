'use client';

/********************** Modules **********************/
import { useState, useEffect, useRef } from "react";
import { usePathname } from "next/navigation";

// Icons
import { MdOutlineDashboard } from "react-icons/md";
import { TbContract, TbArrowBack } from "react-icons/tb";
import { FiVideo } from "react-icons/fi";
import { HiOutlineLink } from "react-icons/hi";
import { IoChatbubblesOutline } from "react-icons/io5";
import { BsStars } from "react-icons/bs";

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
const Studio_Sidebar = () => {
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
        <nav className={` studio-sidebar ${studioSidebarOpen ? "" : "studio-content-shide"} `}>
            <div>
                <div className="studio-icon-logo-container">
                    <Link href={routes.studio.home} className="logo">
                        <img src="/img/icon.svg" alt="Floau Logo" className="studio-logo-img" />
                        <span className="studio-logo-text">Floua Studio</span>
                        <span className="studio-logo-text-extra">Beta</span>
                    </Link>
                </div>

                <div className="studio-sidebar-links-container">
                    <div className="studio-sidebar-title-container">
                        <MdOutlineDashboard className="color-main" size={26} />
                        <span className="studio-sidebar-title">Dashboard</span>
                    </div>

                    <Link href={routes.studio.home} className="studio-sidebar-link-container" data-sidebar-link="home">
                        <span className="studio-sidebar-link-text">Overview</span>
                    </Link>

                    <div className="studio-sidebar-title-container">
                        <FiVideo className="color-main" size={26} />
                        <span className="studio-sidebar-title">Channels</span>
                    </div>

                    <Link href={routes.studio.channels.manage} className="studio-sidebar-link-container" data-sidebar-link="home">
                        <span className="studio-sidebar-link-text">Manage</span>
                    </Link>

                    <div className="studio-sidebar-title-container">
                        <TbContract className="color-main" size={26} />
                        <span className="studio-sidebar-title">Contracts</span>
                    </div>

                    <div className="studio-sidebar-title-container">
                        <IoChatbubblesOutline className="color-main" size={26} />
                        <span className="studio-sidebar-title">Chats</span>
                    </div>

                    <div className="studio-sidebar-title-container">
                        <BsStars className="color-main" size={26} />
                        <span className="studio-sidebar-title">Assistance</span>
                    </div>

                    <div className="studio-sidebar-title-container">
                        <HiOutlineLink className="color-main" size={26} />
                        <span className="studio-sidebar-title">Connections</span>
                    </div>
                </div>
            </div>
            <div>
                <Link href={routes.public.home} className="studio-sidebar-title-container studio-sidebar-go-back">
                    <TbArrowBack className="" size={26} />
                    <span className="studio-sidebar-title">Exit Studio</span>
                </Link>
            </div>
        </nav>
    );
};

/********************** Export **********************/
export default Studio_Sidebar;
