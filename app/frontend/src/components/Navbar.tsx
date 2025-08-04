'use client';

/********************** Modules **********************/
import { usePathname } from "next/navigation";

// Routes
import { routes } from "@/helpers/routes";

// UI
import { use_UI } from "@/context/ui";

/********************** Show **********************/
const hide_navbar_paths = [routes.auth.signup, routes.auth.signin];

/********************** Component **********************/
const Navbar = () => {
    // States
    const { sidebarOpen, toggleSidebar } = use_UI();

    // Check if valid path
    const pathname = usePathname();
    if (hide_navbar_paths.includes(pathname)) return "";

    // DOM
    return (
        <nav className="navbar">

            <div className="icon-logo-container">

                <a href={routes.public.home} className="logo">
                    <img src="/img/icon.svg" alt="Floau Logo" className="logo-img" />
                    <span className="logo-text">Floua</span>
                    <span className="logo-text-extra">Beta</span>
                </a>
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
                <i className={`fa-regular sidebar-toggle-icon ${sidebarOpen ? " fa-bars" : "fa-close"}`}></i>
            </button>

            <div id="navbar-actions">
                <a href={routes.auth.signin} className="btn btn-outline-secondary">Sign in</a>
                <a href={routes.auth.signup} className="btn btn-primary">Sign up</a>
            </div>
        </nav>
    );
};

/********************** Export **********************/
export default Navbar;
