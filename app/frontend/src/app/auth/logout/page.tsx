'use client';

/********************** Modules **********************/
import { useEffect } from "react";

// Routes
import { routes } from "@/helpers/routes";

// Auth
import { useAuth } from "@/context/auth";

/********************** Logout **********************/
const Logout = () => {
    // Auth
    const { logout } = useAuth();

    useEffect(() => {
        const call_logout = async () => {
            await logout();
        }

        call_logout();
    }, [logout]);

    setTimeout(() => {
      window.location.href = routes.public.home;
    }, 2000)

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

          <span className="auth-chage-link-container">Loggin out...</span>
          <span className="auth-chage-link-container">You will be redirected soon!</span>
        </div>

        <span className="auth-brand-full-text-small">No more instrusive ads. Just creator-powered sponsorships.</span>
      </div>
    </div>
  );

};

export default Logout;