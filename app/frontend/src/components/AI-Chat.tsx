'use client';

/********************** Modules **********************/
import React, { useState, useEffect, useRef } from "react";
import { usePathname } from "next/navigation";

// Icons
import { TbDots } from "react-icons/tb";
import { BsStars } from "react-icons/bs";
import { CgClose } from "react-icons/cg";
import { IoSend } from "react-icons/io5";
import { IoMdAdd } from "react-icons/io";
import { GoListUnordered } from "react-icons/go";

// Settings
import { settings } from "@/helpers/settings";

// Routes
import { routes } from "@/helpers/routes";

// AI Chat
import { use_Ai_chat } from "@/context/ai_chat";

// Auth
import { useAuth } from "@/context/auth";

// Api
import { get_data, send_data } from "@/helpers/api";

// Utils
import { truncate_words } from "@/helpers/utils";

// Notifications
import { useNotification } from "@/context/notifications";

/********************** Show **********************/
const hide_chat = [
    routes.auth.signup, routes.auth.signin, routes.auth.logout, routes.auth.verify_path
];

/********************** Component **********************/
const Ai_Chat = () => {
    // Notifications
    const { notify } = useNotification();

    // Structure
    interface Session {
        id: string,
        title: string,
        message_count: string,
        last_message: string,
        last_message_time: string,
        updated_at: string,
        date: string
    };

    interface Chat {
        chat_id: string,
        title: string,
        date: string
    };

    // States
    const { aiChatOpen, toggleAiChat } = use_Ai_chat();
    const [activeTab, setActiveTab] = useState("new_chat");
    const [aiInput, setAiInput] = useState<string>("");
    const [aiChat, setAiChat] = useState<Chat>({
        chat_id: "",
        title: "",
        date: ""
    });

    const [sessions, setSessions] = useState<Session[]>([]);
    const [currentChatId, setCurrentChatId] = useState("");

    // Ref
    const chat_ref = useRef<HTMLDivElement>(null);
    const chat_btn = useRef<HTMLButtonElement>(null);

    // Auth
    const { user } = useAuth();

    // Check if valid path
    const pathname = usePathname();
    if (hide_chat.some(path => pathname.startsWith(path))) return "";

    // Check if is auth
    if (!user) return ""

    // 
    useEffect(() => {
        if (!chat_btn.current) return;

    }, []);

    // Get Chat Session
    const get_chat_session = async (chat_id: string) => {
        const data = await send_data(`/api/ai/chat/${chat_id}`, {}, {
            start: "0",
            end: "15",
        });

        const chat_data = data.chat;

        setAiChat({
            chat_id: chat_data.chat_id,
            title: chat_data.title,
            date: chat_data.date
        });
        setActiveTab("chat_id");
        setCurrentChatId(chat_data.chat_id);
    };

    // Get Chat Sessions
    const get_chat_sessions = async () => {
        // Variables
        let i, session, last_message_time, updated_at, date, sessions = [];

        const data = await get_data("/api/ai/chat/sessions/active", {});

        if (!data) return;

        for (i = 0; i < data.sessions.length; i++) {
            session = data.sessions[i];

            last_message_time = new Date(session.last_message_time).toLocaleDateString("en-US", {
                timeZone: settings.timeZone,
                minute: "2-digit",
                hour: "2-digit",
                day: "2-digit",
                month: "long",
                year: "numeric",
            });

            updated_at = new Date(session.updated_at).toLocaleDateString("en-US", {
                timeZone: settings.timeZone,
                minute: "2-digit",
                hour: "2-digit",
                day: "2-digit",
                month: "long",
                year: "numeric",
            });

            date = new Date(session.date).toLocaleDateString("en-US", {
                timeZone: settings.timeZone,
                minute: "2-digit",
                hour: "2-digit",
                day: "2-digit",
                month: "long",
                year: "numeric",
            });

            sessions.push({
                id: session.id,
                title: session.title,
                message_count: session.message_count,
                last_message: session.last_message,
                last_message_time: last_message_time,
                updated_at: updated_at,
                date: date
            });
        }

        setSessions(sessions);
    };

    // New Chat
    const new_chat = async () => {
        setCurrentChatId("");

        const data = await send_data("/api/ai/chat/create", {}, {
            "title": truncate_words(aiInput)
        });

        return data;
    };

    // New Message
    const new_message = async () => {
        if (!aiInput) return;

        if (!currentChatId) {
            // setCurrentChatId();
            await new_chat()
        }

        setAiInput("");
        notify("New chat created - responses coming soon!", 'info');
    };

    // Handle Change
    const handle_change = (event: React.ChangeEvent<HTMLInputElement>) => {
        setAiInput(event.target.value);
    };

    // Handle keydown
    const handle_key_down = async (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === "Enter") {
            await new_message();
        }
    };

    // DOM
    return (
        <div>
            <button ref={chat_btn} className={`floua-ai-chat-btn ${aiChatOpen ? "swing-out-right-bck" : "fade-in"}`} onClick={() => toggleAiChat()}>
                <span>Assistant</span> <BsStars size={20} />
            </button>

            <div ref={chat_ref} className={`floua-ai-chat-container ${aiChatOpen ? "fade-in" : "hidden"}`}>
                <div className="floua-ai-options-container">
                    <div>
                        <button className="floua-ai-option-btn background-color-red" onClick={() => {
                            toggleAiChat();
                            setAiInput("");
                        }} >
                            <CgClose size={20} />
                        </button>
                    </div>
                    <div className="floua-ai-options-container-right">
                        <button className="floua-ai-option-btn background-color-teal" onClick={() => {
                            setActiveTab("new_chat");
                            setCurrentChatId("");
                            setAiInput("");
                        }}>
                            <IoMdAdd size={22} />
                        </button>
                        <button className="floua-ai-option-btn background-color-blue" onClick={() => {
                            setActiveTab("history");
                            get_chat_sessions();
                            setAiInput("");
                        }}>
                            <GoListUnordered size={20} />
                        </button>
                    </div>
                </div>

                {activeTab == "chat_id" && currentChatId && aiChat && (
                    <div className="floua-ai-chat">
                        <div className="floua-ai-chat-top">
                            <h3 className="floua-ai-chat-top-title">{aiChat.title}</h3>
                        </div>
                        <div className="floua-ai-chat-body">
                        </div>
                        <div className="floua-ai-chat-bottom">
                            <input className="floua-ai-chat-bottom-user-input" placeholder="Message" autoComplete="off" value={aiInput} onChange={handle_change} onKeyDown={handle_key_down} />
                            <button className="floua-ai-chat-bottom-user-btn" onClick={() => new_message()}>
                                <IoSend size={20} />
                            </button>
                        </div>
                    </div>
                )}

                {activeTab == "new_chat" && !currentChatId && (
                    <div className="floua-ai-chat">
                        <div className="floua-ai-chat-top">
                            <h3 className="floua-ai-chat-top-title">Floua Assistant</h3>
                        </div>
                        <div className="floua-ai-chat-body">
                            <div className="floua-ai-chat-body-new">
                                <h3 className="floua-ai-chat-body-new-title">Welcome <span className="color-main">{user.username}</span></h3>
                                <div className="floua-ai-chat-body-new-container">
                                    <p className="floua-ai-chat-body-new-text">Start using our <span className="color-teal">Beta AI</span></p>
                                </div>
                            </div>
                        </div>
                        <div className="floua-ai-chat-bottom">
                            <input className="floua-ai-chat-bottom-user-input" placeholder="Message" autoComplete="off" value={aiInput} onChange={handle_change} onKeyDown={handle_key_down} />
                            <button className="floua-ai-chat-bottom-user-btn" onClick={() => new_message()}>
                                <IoSend size={20} />
                            </button>
                        </div>
                    </div>
                )}

                {activeTab == "history" && (
                    <div className="floua-ai-chat">
                        <div className="floua-ai-chat-top">
                            <h3 className="floua-ai-chat-top-title">History</h3>
                        </div>
                        <div className="floua-ai-chat-body-history">
                            {sessions.map(session => (
                                <div className="floua-ai-chat-body-history-item" key={session.id} onClick={() => get_chat_session(session.id)}>
                                    <span className="floua-ai-chat-body-history-item-title">{session.title}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

/********************** Export **********************/
export default Ai_Chat;
