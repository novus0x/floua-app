'use client';

/********************** Modules **********************/
import { createContext, useContext, useState, ReactNode } from "react";

/********************** Structures **********************/
type AI_chat_context_type = {
    aiChatOpen: boolean;
    toggleAiChat: () => void;
};

/********************** Variables **********************/
const AI_chat_context = createContext<AI_chat_context_type | undefined >(undefined);

/********************** Function **********************/
export const AI_chat_provider = ({ children }: { children: ReactNode }) => {
    const [aiChatOpen, setAiChatOpen] = useState(false);

    const toggleAiChat = () => setAiChatOpen(prev => !prev);

    return (
        <AI_chat_context.Provider value={{ aiChatOpen, toggleAiChat }}>
            { children }
        </AI_chat_context.Provider>
    );
};

/********************** Export **********************/
export const use_Ai_chat = () => {
    const context = useContext(AI_chat_context);
    if (!context) throw new Error("use_Ai_chat must be used within a AI_chat_provider");
    return context;
}
