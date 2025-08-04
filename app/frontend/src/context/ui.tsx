'use client';

/********************** Modules **********************/
import { createContext, useContext, useState, ReactNode } from "react";

/********************** Structures **********************/
type UI_context_type = {
    sidebarOpen: boolean;
    toggleSidebar: () => void;
};

/********************** Variables **********************/
const UI_context = createContext<UI_context_type | undefined >(undefined);

/********************** Function **********************/
export const UI_provider = ({ children }: { children: ReactNode }) => {
    const [sidebarOpen, setSidebarOpen] = useState(true);

    const toggleSidebar = () => setSidebarOpen(prev => !prev);

    return (
        <UI_context.Provider value={{ sidebarOpen, toggleSidebar }}>
            { children }
        </UI_context.Provider>
    );
};

/********************** Export **********************/
export const use_UI = () => {
    const context = useContext(UI_context);
    if (!context) throw new Error("use_IU must be used within a UI_provider");
    return context;
}
