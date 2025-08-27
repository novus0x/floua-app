/********************** Routes **********************/
export const routes = {
    // Public
    public: {
        home: "/",
        trending: "/trending",
        explore: "/explore",
        watch: (id: string) => `/watch?id=${id}`,
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

        home: (tag: string) => `/@${tag}`, //"/channel", // (channel_name: string) => `/@${channel_name}`
    },

    // Studio
    studio: {
        home: "/studio",
        channels: {
            manage: "/studio/channels/manage",
            manage_tag: (tag: string) => `/studio/channels/manage/${tag}`,

            upload_tag: (tag: string) => `/studio/channels/upload/${tag}`,
            check_upload_tag: (tag: string, id: string) => `/studio/channels/upload/${tag}/status/${id}`,
        },
    },

    // Test
    test: "/test",
}
