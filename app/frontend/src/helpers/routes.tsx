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

    // Test
    test: "/test",
}
