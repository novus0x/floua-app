'use client';

/********************** Modules **********************/
import { createContext, useContext, useEffect, useState } from "react";

// API
import { get_data } from "../helpers/api";

// Settings
import { settings } from "../helpers/settings";

/********************** Variables **********************/
const AuthContext = createContext();

/********************** Function **********************/
export function Auth_provider({ children }) {
    const [user, setUser] = useState(null);
    const [userLoading, setUserLoading] = useState(true);

    // Get & Check token
    useEffect(() => {
        const get_session = async () => {

            const data = await get_data("/api/accounts/validate", {});

            if (data?.user) setUser(data.user);
            else {
                setUser(null);
            }

            if (data?.expired) await get_data("/api/users/logout", {});

            setUserLoading(false);
        };

        get_session();
    }, []);

    const logout = async () => {
        await get_data("/api/users/logout", {});
        setUser(null);
    }

    return (
        <AuthContext.Provider value={{ user, logout, userLoading }}>
            { !userLoading && children }
        </AuthContext.Provider>
    );
}

/********************** Export **********************/
export function useAuth() {
    return useContext(AuthContext);
}
