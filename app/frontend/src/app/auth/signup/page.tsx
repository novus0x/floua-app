'use client';

/********************** Modules **********************/
import { useState } from "react";
import { useRouter } from "next/navigation";

// DOM
import Link from "next/link";

// Routes
import { routes } from "@/helpers/routes";

// Notifications
import { useNotification } from "@/context/notifications";

// API
import { send_data } from "@/helpers/api";

/********************** Signup **********************/
const Signup = () => {
  // Router
  const router = useRouter();

  // Notifications
  const { notify } = useNotification();

  // User information
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirm_password: '',
    date_of_birth: '',
  });

  // Submit status
  const [loading, setLoading] = useState(false);

  // Update values
  const handle_change = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  // Submit form
  const hanle_submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // Request
    const data = await send_data("/api/users/signup", {}, formData, notify);

    if (data) {
      setTimeout(() => {
        router.push(routes.auth.signin);
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

          <label htmlFor="username" className="form-auth-input-hint">Username</label>
          <input type="text" name="username" placeholder="Example123" value={formData.username} onChange={handle_change} id="username" className="form-auth-input" required />
          <label htmlFor="email" className="form-auth-input-hint">Email</label>
          <input type="email" name="email" placeholder="example@gmail.com" value={formData.email} onChange={handle_change} id="email" className="form-auth-input" required />
          <label htmlFor="password" className="form-auth-input-hint">Password</label>
          <input type="password" name="password" placeholder="************" value={formData.password} onChange={handle_change} id="password" className="form-auth-input" required />
          <label htmlFor="confirm_password" className="form-auth-input-hint">Confirm Password</label>
          <input type="password" name="confirm_password" placeholder="************" value={formData.confirm_password} onChange={handle_change} id="confirm_password" className="form-auth-input" required />
          <label htmlFor="date_of_birth" className="form-auth-input-hint">Date of birth</label>
          <input type="date" name="date_of_birth" value={formData.date_of_birth} onChange={handle_change} id="date_of_birth" className="form-auth-input" required />
          <button type="submit" disabled={loading} className="btn btn-primary">{loading ? 'Registering...' : 'Sign up!'}</button>
          <span className="auth-chage-link-container">Already register? <Link href={routes.auth.signin} className="auth-chage-link">Sign in!</Link></span>
        </form>

        <span className="auth-brand-full-text-small">No more instrusive ads. Just creator-powered sponsorships.</span>
      </div>
    </div>
  );
};

export default Signup;