'use client';

/********************** Modules **********************/
import { useState, useEffect, useRef } from "react";
import { usePathname } from "next/navigation";

// Icons
import { FaBell, FaBars } from "react-icons/fa";
import { FiLogOut, FiSettings, FiPlus } from "react-icons/fi";
import { MdOutlineClose } from "react-icons/md";

// DOM
import Link from "next/link";

// Routes
import { routes } from "@/helpers/routes";

// UI
import { use_UI } from "@/context/ui";

// Auth
import { useAuth } from "@/context/auth";

/********************** Show **********************/
const hide_navbar_paths = [routes.auth.signup, routes.auth.signin, routes.auth.logout];

/********************** Component **********************/
const Navbar = () => {
    // States
    const { sidebarOpen, toggleSidebar } = use_UI();
    const [userMenu, setUserMenu] = useState(false);
    const [userNotifications, setUserNotifications] = useState(false);

    // Ref
    const menu_ref = useRef<HTMLDivElement>(null);
    const notify_ref = useRef<HTMLDivElement>(null);

    // Auth
    const { user } = useAuth();

    // User menu
    const toggle_user_menu = () => {
        setUserMenu(prev => !prev);
        setUserNotifications(false);
    };

    const toggle_notifications = () => {
        setUserNotifications(prev => !prev);
        setUserMenu(false);
    };

    useEffect(() => {
        const handle_click_outside = (event: MouseEvent) => {
            if (menu_ref.current && !menu_ref.current.contains(event.target as Node)) setUserMenu(false);
            if (notify_ref.current && !notify_ref.current.contains(event.target as Node)) setUserNotifications(false);
        };

        document.addEventListener("mousedown", handle_click_outside);
        return () => document.removeEventListener("mousedown", handle_click_outside);
    }, [userMenu]);

    // Check if valid path
    const pathname = usePathname();
    if (hide_navbar_paths.includes(pathname)) return "";

    // DOM
    return (
        <nav className="navbar">
            <div className="icon-logo-container">
                <Link href={routes.public.home} className="logo">
                    <img src="/img/icon.svg" alt="Floau Logo" className="logo-img" />
                    <span className="logo-text">Floua</span>
                    <span className="logo-text-extra">Beta</span>
                </Link>
            </div>

            {/* <form className="search-container">
                <input type="text" name="query" placeholder="Search..." className="search" id="search-result-input" />
                    <div className="search-backdrop hidden" id="search-backdrop"></div>
                    <button type="button" id="search-btn">
                        <i className="fa-regular fa-magnifying-glass search-icon"></i>
                    </button>
                    <div className="search-results hidden" id="search-results">
                        <div className="search-results-links">
                            <span className="search-result-text" id="search-result-link-input"></span>
                        </div>
                        <div className="search-results-links" id="search-results-links"></div>
                    </div>
            </form> */}

            <button className="btn sidebar-toggle" onClick={() => toggleSidebar()} >
                {sidebarOpen ? (
                    <FaBars className="sidebar-toggle-icon"/>
                ) : (
                    <MdOutlineClose className="sidebar-toggle-icon" />
                )}
            </button>

            <div className="navbar-actions">
                {user ? (
                    <div className="navbar-user-session">
                        <span className="navbar-user-session-points">{user.points} <img src="/img/point.svg" alt="Floua point - FP" className="navbar-user-session-points-image" /></span>
                        <div ref={notify_ref} className="navbar-user-notifications-container-ref">
                            <button className="navbar-user-notifications-container" onClick={toggle_notifications}>
                                <FaBell className="navbar-user-notifications-icon" />
                            </button>
                        </div>
                        <div ref={menu_ref} className="navbar-user-avatar-container-ref">
                            <button className="navbar-user-avatar-container" onClick={toggle_user_menu}>
                                <div className="navbar-user-avatar-overlay"></div>
                                <img src={user.avatar_url} alt="User avatar" className="navbar-user-avatar" />
                            </button>
                            <div className={`navbar-user-avatar-extra-container ${userMenu ? "" : "hidden"}`}>
                                <div className="navbar-user-avatar-extra-account">
                                    <img src={user.avatar_url} alt="User avatar" className="navbar-user-avatar-extra-account-avatar" />
                                    <div className="navbar-user-avatar-extra-account-info">
                                        <span className="navbar-user-avatar-extra-username">{user.username}</span>
                                        <span className="navbar-user-avatar-extra-email">{user.email}</span>
                                    </div>
                                </div>
                                <div className="navbar-user-avatar-extra-divider"></div>
                                <div className="navbar-user-avatar-extra-links">
                                    {user.has_channel ? (
                                        <Link href="#" className="navbar-user-avatar-extra-link"><i className="fa-regular fa-video navbar-user-avatar-extra-link-icon"></i> Go to my channel</Link>
                                    ) : (
                                        <Link href="#" className="navbar-user-avatar-extra-link"><FiPlus className="navbar-user-avatar-extra-link-icon" size={25} /> Create Channel</Link>
                                    )}
                                    <Link href={routes.account.home} className="navbar-user-avatar-extra-link"><FiSettings className="navbar-user-avatar-extra-link-icon" size={23} /> Account</Link>
                                    <Link href={routes.auth.logout} className="navbar-user-avatar-extra-link-logout"><FiLogOut className="navbar-user-avatar-extra-link-icon" size={24} /> Logout</Link>
                                </div>
                            </div>
                        </div>
                    </div>
                ) : (
                    <>
                        <Link href={routes.auth.signin} className="btn btn-outline-secondary">Sign in</Link>
                        <Link href={routes.auth.signup} className="btn btn-primary navbar-btn-signup">Sign up</Link>
                    </>
                )}
            </div>
        </nav>
    );
};

/********************** Export **********************/
export default Navbar;
