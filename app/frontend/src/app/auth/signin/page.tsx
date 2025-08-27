'use client';

/********************** Modules **********************/
import { useState } from "react";

// DOM
import Link from "next/link";

// Routes
import { routes } from "@/helpers/routes";

// Notifications
import { useNotification } from "@/context/notifications";

// API
import { send_data } from "@/helpers/api";

// Utils
import { set_cookie } from "@/helpers/utils";

/********************** Signin **********************/
const Signin = () => {
  // Notifications
  const { notify } = useNotification();

  // Submit status
  const [loading, setLoading] = useState(false);

  // User information
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    keep_session: false,
  });

  // Update values
  const handle_change = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  // Submit form
  const hanle_submit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);

    const form = e.currentTarget;

    const data_to_send = {
      email: formData.email,
      password: formData.password,
      expires: form.keep_session.checked ? "1" : "0",
    }

    // Request
    const data = await send_data("/api/users/signin", {}, data_to_send, notify);

    if (data) {
      setTimeout(() => {
        set_cookie("authenticated", "yes");
        window.location.href = routes.public.home;
      }, 1000);
    } else setLoading(false);
  };

  // DOM
  return (
    <div className="auth-container">
      <video src="/videos/video_background.mp4" autoPlay loop muted className="auth-video-background"></video>
      <div className="auth-video-overlay"></div>

      <div className="auth-container-form">
        <form onSubmit={hanle_submit} className="form-auth-container" >
          <div className="auth-brand-full">
            <Link href={routes.public.home} className="auth-brand-full-logo-container">
              <img src="/img/icon.svg" alt="Floua Logo" className="auth-brand-full-logo" />
              <span className="auth-brand-full-text">Floua</span>
              <span className="auth-brand-full-text-extra">Beta</span>
            </Link>
          </div>

          <label htmlFor="email" className="form-auth-input-hint">Email</label>
          <input type="email" name="email" placeholder="example@gmail.com" value={formData.email} onChange={handle_change} id="email" className="form-auth-input" required />
          <label htmlFor="password" className="form-auth-input-hint">Password</label>
          <input type="password" name="password" placeholder="************" value={formData.password} onChange={handle_change} id="password" className="form-auth-input" required />
          <div className="auth-keep-session-container">
            <label htmlFor="keep_session" className="">Keep the session active?</label>
            <input type="checkbox" name="keep_session" placeholder="************" onChange={handle_change} id="keep_session" className="form-auth-input-session" />
          </div>
          <button type="submit" disabled={loading} className="btn btn-primary">{loading ? 'Login...' : 'Sign in!'}</button>
          <span className="auth-chage-link-container">Haven't you registered yet? <Link href={routes.auth.signup} className="auth-chage-link">Sign up!</Link></span>
        </form>

        <span className="auth-brand-full-text-small">No more instrusive ads. Just creator-powered sponsorships.</span>
      </div>
    </div>
  );
};

export default Signin;