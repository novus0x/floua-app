'use client';

/********************** Modules **********************/
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

// DOM
import Link from "next/link";

// Routes
import { routes } from "@/helpers/routes";

// Auth
import { useAuth } from "@/context/auth";

// Notifications
import { useNotification } from "@/context/notifications";

// API
import { send_data } from "@/helpers/api";

/********************** Account **********************/
const Account = () => {
  // Auth
  const { user } = useAuth();

  // Router
  const router = useRouter();

  // Notifications
  const { notify } = useNotification();

  // States
  const [formData, setFormData] = useState({
    name: '',
    tag: '',
    description: '',
  });

  const [channelTag, setChannelTag] = useState("example_123");

  // Generate @
  const generate_tag = (name: string) => {
    let cleaned = name.toLowerCase().replace(/[^a-z0-9_-]/g, "");
    return `${cleaned}`;
  }

  // Submit status
  const [loading, setLoading] = useState(false);

  // Update tag
  const update_tag = (name: string) => {
    formData.tag = generate_tag(name);
    setChannelTag(formData.tag);
  }

  // Update values
  const handle_change = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    if (e.target.tagName === "INPUT") update_tag(e.target.value);
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  // Submit form
  const create_channel = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    if (formData.description == "") formData.description = "No description";

    // Request
    const data = await send_data("/api/channels/create", {}, formData, notify);

    if (data) {
      setTimeout(() => {
        router.push(routes.public.home);
      }, 1000);
    } else setLoading(false);
    setLoading(false);
  }

  // DOM
  return (
    <div className="content">
      <div className="create-channel-container">
        <form onSubmit={create_channel} className="create-channel-form">
          <span className="create-channel-text">Channel name</span>
          <div className="create-channel-form-input-container">
            <input type="text" name="name" className="create-channel-input" placeholder="Example 123" value={formData.name} onChange={handle_change} required />
            <span className="create-channel-looks-like">It will look like this: /@{channelTag}</span>
          </div>
          <span className="create-channel-text">Channel description</span>
          <div className="create-channel-form-input-container">
            <textarea name="description" className="create-channel-input" placeholder="Description (Optional)" value={formData.description} onChange={handle_change}></textarea>
          </div>
          <button type="submit" className="create-channel-btn" disabled={loading}>{loading ? 'Creating...' : 'Create Channel!'}</button>
          <span className="create-channel-slogan">Your activity here makes a difference. Every channel created helps us to improve!</span>
        </form>
      </div>
    </div>
  );
};

export default Account;