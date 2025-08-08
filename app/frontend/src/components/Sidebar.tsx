'use client';

/********************** Modules **********************/
import { usePathname } from "next/navigation";

// Icons
import { FaFire, FaClockRotateLeft } from "react-icons/fa6"
import { FaCompactDisc, FaUsers, FaList } from "react-icons/fa"
import { HiMiniHome } from "react-icons/hi2"

// DOM
import Link from "next/link";

// Routes
import { routes } from "@/helpers/routes";

// UI
import { use_UI } from "@/context/ui";

// Auth
import { useAuth } from "@/context/auth";

/********************** Show **********************/
const hide_sidebar_paths = [routes.auth.signup, routes.auth.signin, routes.auth.logout];

/********************** Component **********************/
const Sidebar = () => {
    // States
    const { sidebarOpen, toggleSidebar } = use_UI();

    // Auth
    const { user } = useAuth();

    // Check if valid path
    const pathname = usePathname();
    if (hide_sidebar_paths.includes(pathname)) return "";

    // DOM
    return (
        <nav className={`sidebar ${sidebarOpen ? "" : "sidebar-hide"} `}>
            <div>
                <Link href={routes.public.home} className={`sidebar-link-container ${pathname == routes.public.home ? "sidebar-link-container-active" : ""}`} data-sidebar-link="home">
                    <div className="sidebar-link-icon-container">
                        <HiMiniHome className="color-teal" size={32}/>
                    </div>
                    <span className="sidebar-link-text">Home</span>
                </Link>

                <Link href={routes.public.trending} className={`sidebar-link-container ${pathname == routes.public.trending ? "sidebar-link-container-active" : ""}`} data-sidebar-link="trending">
                    <div className="sidebar-link-icon-container">
                        <FaFire className="color-orange" size={27}/>
                    </div>
                    <span className="sidebar-link-text">Trending</span>
                </Link>

                <Link href={routes.public.explore} className={`sidebar-link-container ${pathname == routes.public.explore ? "sidebar-link-container-active" : ""}`} data-sidebar-link="explore">
                    <div className="sidebar-link-icon-container">
                        <FaCompactDisc className="color-yellow" size={27} />
                    </div>
                    <span className="sidebar-link-text">Explore</span>
                </Link>

                {user ? (
                    <>
                        <Link href={routes.public_session.following} className={`sidebar-link-container ${pathname == routes.public_session.following ? "sidebar-link-container-active" : ""}`} data-sidebar-link="following">
                            <div className="sidebar-link-icon-container">
                                <FaUsers className="color-lime-green" size={27} />
                            </div>
                            <span className="sidebar-link-text">Following</span>
                        </Link>
                        <Link href={routes.public_session.playlists} className={`sidebar-link-container ${pathname == routes.public_session.playlists ? "sidebar-link-container-active" : ""}`} data-sidebar-link="playlists">
                            <div className="sidebar-link-icon-container">
                                <FaList className="color-main" size={27} />
                            </div>
                            <span className="sidebar-link-text">Playlists</span>
                        </Link>
                        <Link href={routes.public_session.history} className={`sidebar-link-container ${pathname == routes.public_session.history ? "sidebar-link-container-active" : ""}`} data-sidebar-link="history">
                            <div className="sidebar-link-icon-container">
                                <FaClockRotateLeft className="color-blue" size={27} />
                            </div>
                            <span className="sidebar-link-text">History</span>
                        </Link>
                    </>
                ) : (
                    <>
                    </>
                )}

                <div id="sidebar-actions">
                    {user ? (
                        <>
                        </>
                    ) : (
                        <>
                            <Link href={routes.auth.signin} className="btn btn-outline-secondary">Sign in</Link>
                            <Link href={routes.auth.signup} className="btn btn-primary">Sign up</Link>
                        </>
                    )}

                </div>
            </div>
            {user ? (
                <>
                    {/* <Link href="#" className="btn btn-primary">{session.email}</Link> */}
                </>
            ) : (
                <>
                    <span className="sidebar-extra">More features available after loggin in!</span>
                </>
            )}

        </nav >
    );
};

/********************** Export **********************/
export default Sidebar;
