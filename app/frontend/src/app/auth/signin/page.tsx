'use client';

/********************** Modules **********************/
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

// Settings
import { settings } from "@/helpers/settings";

// Routes
import { routes } from "@/helpers/routes";

// Notifications
import { useNotification } from "@/context/notifications";

// Utils
import { set_cookie } from "@/helpers/utils";

/********************** Signup **********************/
const Signup = () => {
  // Router
  const router = useRouter();

  // Notifications
  const { notify } = useNotification();

  // User information
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    keep_session: false,
  });

  // Submit status
  const [loading, setLoading] = useState(false);

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

    try {
      const res = await fetch(`${settings.api_url}/api/users/signin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data_to_send),
      });

      const data = await res.json();
      if (res.status == 400) {
        if (!data.details) { // General error
          notify(data.message, 'alert');
        } else { // Details about error
          let i;
          const details = data.details;

          for (i = 0; i < details.length; i++) {
            notify(details[i].message, 'alert');
          }
        }
      } else {
        notify(data.message, 'success');
        set_cookie(data.data.token);
        setTimeout(() => {
          router.push(routes.public.home);
        }, 1000);
      }

    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <video src="/videos/video_background.mp4" autoPlay loop muted className="auth-video-background"></video>
      <div className="auth-video-overlay"></div>

      <div className="auth-container-form">
        <form onSubmit={hanle_submit} className="form-auth-container" >
          <div className="auth-brand-full">
            <a href={routes.public.home} className="auth-brand-full-logo-container">
              <img src="/img/icon.svg" alt="Floua Logo" className="auth-brand-full-logo" />
              <span className="auth-brand-full-text">Floua</span>
              <span className="auth-brand-full-text-extra">Beta</span>
            </a>
          </div>

          <label htmlFor="email" className="form-auth-input-hint">Email</label>
          <input type="email" name="email" placeholder="example@gmail.com" value={formData.email} onChange={handle_change} id="email" className="form-auth-input" required/>
          <label htmlFor="password" className="form-auth-input-hint">Password</label>
          <input type="password" name="password" placeholder="************" value={formData.password} onChange={handle_change} id="password" className="form-auth-input" required/>
          <div className="auth-keep-session-container">
            <label htmlFor="keep_session" className="">Keep the session active?</label>
            <input type="checkbox" name="keep_session" placeholder="************" onChange={handle_change} id="keep_session" className="form-auth-input-session" />
          </div>
          <button type="submit" disabled={loading} className="btn btn-primary">{loading ? 'Login...' : 'Sign in!'}</button>
          <span className="auth-chage-link-container">Haven't you registered yet? <a href={routes.auth.signup} className="auth-chage-link">Sign up!</a></span>
        </form>

        <span className="auth-brand-full-text-small">No more instrusive ads. Just creator-powered sponsorships.</span>
      </div>
    </div>
  );
};

export default Signup;