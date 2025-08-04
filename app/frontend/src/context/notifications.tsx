'use client';

/********************** Modules **********************/
import { v4 as uuidv4 } from 'uuid';
import { createContext, useContext, useState, ReactNode } from "react";

/********************** Structures **********************/
type notification_type = "info" | "success" | "warning" | "alert";

interface Notification {
    id: string;
    message: string;
    type: notification_type;
    isExiting?: boolean;
}

/********************** Variables **********************/
const notification_context = createContext<any>(null);

/********************** Function **********************/
export const Notification_provider = ({ children }: { children: ReactNode }) => {
    const [notifications, setNotifications] = useState<Notification[]>([]);

    const notify = (message: string, type: notification_type = 'info') => {
        const id = uuidv4();
        const new_notification = { id, message, type };
        setNotifications((prev) => [...prev, new_notification]);

        setTimeout(() => {
            setNotifications((prev) => prev.map((n) => n.id == id ? { ...n, isExiting: true } : n));
        }, 3500);

        setTimeout(() => {
            setNotifications((prev) => prev.filter((n) => n.id != id));
        }, 4500);
    };

    return (

        <notification_context.Provider value={{ notify }}>
            { children }
            <div className="notification-container">
                { notifications.map((n) => (
                    <div key={n.id} className={`notification notification-${n.type} slide-in-right ${n.isExiting ? 'slide-out-right' : ''}`}>{ n.message }</div>
                )) }
            </div>
        </notification_context.Provider>

    );
}

/********************** Export **********************/
export const useNotification = () => useContext(notification_context);
