'use client';

/********************** Modules **********************/
import { useState, useEffect } from "react";

// Icons
import { FaLink, FaLock, FaVideo, FaUser, FaDotCircle } from "react-icons/fa";
import { FiSettings } from "react-icons/fi";
import { PiTidalLogoFill, PiTreasureChestFill } from "react-icons/pi";
import { SiKick } from "react-icons/si";

// DOM
import Link from "next/link";

// Routes
import { routes } from "@/helpers/routes";

// Notifications
import { useNotification } from "@/context/notifications";

// Auth
import { useAuth } from "@/context/auth";

// API
import { get_data, send_data } from "@/helpers/api";

/********************** Account **********************/
const Account = () => {
  // Notifications
  const { notify } = useNotification();

  // Auth
  const { user } = useAuth();

  // Structure
  interface Session {
    id: string,

    is_active: boolean,
    expires_at: string,

    ip_addr: string,
    user_agent: string,
    location: string,

    last_used_at: string,
    date: string,

    os_name: string,
    os_version: string,
    device_name: string,
    device_vendor: string,
    device_model: string,
    device_mobile: boolean,
    device_tablet: boolean,
    device_pc: boolean,
    browser_name: string,
    browser_version: string,
  }

  // States
  const [activeTab, setActiveTab] = useState("general");
  const [sessions, setSessions] = useState<Session[]>([]);

  const [isLogginTrackingChecked, setisLogginTrackingChecked] = useState(user.user_session_extra);

  // Member since
  const registered_date = new Date(user.date);
  const formated_registered_date = registered_date.toLocaleDateString("en-US", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  })

  // API calls
  const get_login_sessions = async () => {

    // Variables
    let i, last_used, expire_at, created, session, sessions = [];

    // Request
    const data = await get_data("/api/accounts/login-tracking", {});

    for (i = 0; i < data.sessions.length; i++) {
      session = data.sessions[i];

      // Format Date --> String
      last_used = new Date(session.last_used_at).toLocaleDateString("en-US", {
        minute: "2-digit",
        hour: "2-digit",
        day: "2-digit",
        month: "long",
        year: "numeric",
      });

      if (session.expires_at) {
        expire_at = new Date(session.expires_at).toLocaleDateString("en-US", {
          minute: "2-digit",
          hour: "2-digit",
          day: "2-digit",
          month: "long",
          year: "numeric",
        });
      } else expire_at = "No expire";

      created = new Date(session.date).toLocaleDateString("en-US", {
        minute: "2-digit",
        hour: "2-digit",
        day: "2-digit",
        month: "long",
        year: "numeric",
      });

      // Add
      sessions.push({
        id: session.id,

        is_active: session.is_active,
        expires_at: expire_at,

        ip_addr: session.ip_addr,
        user_agent: session.user_agent,
        location: session.location,

        last_used_at: last_used,
        date: created,

        os_name: session.os_name,
        os_version: session.os_name,
        device_name: session.device_name,
        device_vendor: session.device_vendor,
        device_model: session.device_model,
        device_mobile: session.device_mobile,
        device_tablet: session.device_tablet,
        device_pc: session.device_pc,
        browser_name: session.browser_name,
        browser_version: session.browser_version,
      })
    }

    setSessions(sessions);
  }

  const deactivate_session = async (session_id: string) => {
    // Request
    const data = await send_data("/api/accounts/deactivate-session", {}, {session_id: session_id}, notify);
    if(data.current_session) window.location.href = routes.auth.logout;

    await get_login_sessions();
  }

  // Active & Deactivate Session Tracking
  const session_tracking_update_state = async () => {
    const data = await send_data("/api/accounts/login-tracking", {}, {
      login_tracking_option: isLogginTrackingChecked ? "0" : "1",
    }, notify);
    setisLogginTrackingChecked(!isLogginTrackingChecked);
  };

  return (
    <div className="content">
      {user.email_verified ? (<></>) : (
        <div className="user-activate-account-container">
          Please verify your account now!
        </div>
      )}

      <div className="content-title-container">
        <span className="content-title"><FiSettings className="content-title-icon color-blue" /> Settings</span>
      </div>

      <div className="account-container">
        <div className="account-options">
          <span className="account-option-title">
            <FaUser className="account-option-title-icon color-main" size={25} /> Account
          </span>
          <button className={`account-option ${activeTab == "general" ? "account-option-active" : ""}`} onClick={() => setActiveTab("general")}>
            General
          </button>
          <span className="account-option-title">
            <FaVideo className="account-option-title-icon color-main" size={25} /> Channel
          </span>
          {user.has_channel ? (
            <button className={`account-option ${activeTab == "channel_overview" ? "account-option-active" : ""}`} onClick={() => setActiveTab("channel_overview")}>
              Overview
            </button>
          ) : (
            <button className={`account-option ${activeTab == "create_channel" ? "account-option-active" : ""}`} onClick={() => setActiveTab("create_channel")}>
              Create Channel
            </button>
          )}
          <span className="account-option-title">
            <FaLock className="account-option-title-icon color-main" size={25} /> Security
          </span>
          <button className={`account-option ${activeTab == "login_tracking" ? "account-option-active" : ""}`} onClick={() => { setActiveTab("login_tracking"); get_login_sessions(); }}>
            Login Tracking
          </button>
          <button className={`account-option ${activeTab == "change_password" ? "account-option-active" : ""}`} onClick={() => setActiveTab("change_password")}>
            Change Password
          </button>
          <span className="account-option-title">
            <PiTreasureChestFill className="account-option-title-icon color-main" size={30} /> Floua Points
          </span>
          <button className="account-option">
            Get
          </button>
          <button className="account-option">
            Transactions
          </button>
          <button className="account-option">
            Withdraw
          </button>
          <span className="account-option-title">
            <FaLink className="account-option-title-icon color-main" size={25} /> Connections
          </span>
          <button className="account-option">
            <SiKick className="color-lime-green account-option-icon" size={20} /> Kick
          </button>
          <button className="account-option">
            <PiTidalLogoFill className="color-white account-option-icon" size={25} /> Tidal
          </button>
          <button className="account-option">
            Others
          </button>
        </div>

        <div className="account-data">

          {activeTab == "general" && (
            <div className="account-data-general-container">
              <div>
                <span className="account-data-general-section-title">Profile Preview</span>
                <div className="account-data-general-basic-container">
                  <img src={user.avatar_url} alt="User avatar" className="account-data-general-basic-avatar" />
                  <div className="account-data-general-basic-info">
                    <span className="account-data-general-basic-info-username">{user.username}</span>
                    <span>{user.email}</span>
                  </div>
                </div>
              </div>
              <div>
                <span className="account-data-general-section-title">Biography</span>
                <div className="account-data-general-basic-container">
                  {user.bio ? (
                    <span>{user.bio}</span>
                  ) : (
                    <span>You haven't added your bio yet.</span>
                  )}
                  {user.bio ? "hey" : ""}
                </div>
              </div>

              <div>
                <span className="account-data-general-section-title">Points</span>
                <div className="account-data-general-basic-container">
                  <span>{user.points}</span>
                </div>
              </div>

              <div>
                <span className="account-data-general-section-title">Member Since</span>
                <div className="account-data-general-basic-container">
                  <span>{formated_registered_date}</span>
                </div>
              </div>
            </div>
          )}

          {activeTab == "create_channel" && (
            <div>Create Channel</div>
          )}

          {activeTab == "login_tracking" && (
            <div className="account-data-loggin-tracking-container">
              <span className="account-data-loggin-tracking-section-title">Login Tracking - <span className="color-main">{isLogginTrackingChecked ? "Activated" : "Deactivated"}</span></span>
              <div className="account-data-loggin-tracking-active-deactivate" onClick={session_tracking_update_state}>
                <FaDotCircle className={`account-data-loggin-tracking-active-deactivate-icon color-main ${isLogginTrackingChecked ? "account-data-loggin-tracking-active-deactivate-icon-active" : ""} `} size={30} />
              </div>

              <span className="account-data-loggin-tracking-section-title">Login History <span className="account-data-loggin-tracking-section-title-extra">Last 10 sessions</span></span>

              {sessions.map(session => (
                <div className="account-data-loggin-tracking" key={session.id}>
                  {session.is_active ? (
                    <p>
                      <span className="color-lime-green">Active</span> (<button className="color-orange account-data-loggin-tracking-deactivate-btn" onClick={() => deactivate_session(session.id)}>Deactivate</button>)
                    </p>
                  ) : (<span className="color-red">Inactive</span>)}
                  <p>New connection from: {session.ip_addr}</p>
                  <p>Location: {session.location}</p>
                  <p>Operating System: {session.os_name}</p>
                  <p>Device name: {session.device_name} </p>
                  <p>Browser info: {session.browser_name} {session.browser_version}</p>
                  <p>Used last: {session.last_used_at}</p>
                  <p>Expires at: {session.expires_at}</p>
                  <p>Created: {session.date}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab == "change_password" && (
            <div>Change Password</div>
          )}

        </div>
      </div>
    </div>
  );
};

export default Account;