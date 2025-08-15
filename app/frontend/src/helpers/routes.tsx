/********************** Routes **********************/
export const routes = {
    // Public
    public: {
        home: "/",
        trending: "/trending",
        explore: "/explore",
    },

    // Auth
    auth: {
        signin: "/auth/signin",
        signup: "/auth/signup",
        logout: "/auth/logout",
        
        verify: (id: string) => `/auth/verify/${id}`,
        verify_path: "/auth/verify",
    },
    
    // Public but session required
    public_session: {
        following: "/following",
        playlists: "/playlists",
        history: "/history",
    },

    // Account
    account: {
        home: "/account",
    },

    // Channel
    channel: {
        opts: {
            create: "/channel/create",
        },

        home: "/channel", // (channel_name: string) => `/@${channel_name}`
    },

    // Test
    test: "/test",
}
