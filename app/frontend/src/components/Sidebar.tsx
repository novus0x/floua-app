'use client';

/********************** Modules **********************/
import { usePathname } from "next/navigation";

// Routes
import { routes } from "@/helpers/routes";

// UI
import { use_UI } from "@/context/ui";

/********************** Show **********************/
const hide_sidebar_paths = [routes.auth.signup, routes.auth.signin];

/********************** Component **********************/
const Sidebar = () => {
    // States
    const { sidebarOpen, toggleSidebar } = use_UI();

    // Check if valid path
    const pathname = usePathname();
    if (hide_sidebar_paths.includes(pathname)) return "";
    

    // DOM
    return (
        <nav className={`sidebar ${sidebarOpen ? "" : "sidebar-hide"} `}>
            <div>
                <a href={routes.public.home} className="sidebar-link-container" data-sidebar-link="home">
                    <div className="sidebar-link-icon-container">
                        <i className="fa-solid fa-home sidebar-link-icon color-teal"></i>
                    </div>
                    <span className="sidebar-link-text">Home</span>
                </a>

                <a href={routes.public.trending} className="sidebar-link-container" data-sidebar-link="trending">
                    <div className="sidebar-link-icon-container">
                        <i className="fa-solid fa-fire-flame-curved sidebar-link-icon color-orange"></i>
                    </div>
                    <span className="sidebar-link-text">Trending</span>
                </a>

                <a href={routes.public.explore} className="sidebar-link-container" data-sidebar-link="explore">
                    <div className="sidebar-link-icon-container">
                        <i className="fa-solid fa-compact-disc sidebar-link-icon color-yellow"></i>
                    </div>
                    <span className="sidebar-link-text">Explore</span>
                </a>

                <div id="sidebar-actions">
                    <a href={routes.auth.signin} className="btn btn-outline-secondary">Sign in</a>
                    <a href={routes.auth.signup} className="btn btn-primary">Sign up</a>
                </div>
            </div>
            <span className="sidebar-extra">More features available after loggin in!</span>
        </nav >
    );
};

/********************** Export **********************/
export default Sidebar;
