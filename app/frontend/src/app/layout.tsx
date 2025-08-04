/********************** Modules **********************/
import type { Metadata } from "next";

import { FC, PropsWithChildren, ReactNode } from "react";

// Styles
import "@/../public/css/globals.css";
import "@/../public/css/animations.css"

// Components
import Navbar from "@/components/Navbar";
import Sidebar from "@/components/Sidebar";

// UI
import { UI_provider } from "@/context/ui";
import { Notification_provider } from "@/context/notifications";

/********************** SEO **********************/
export const metadata: Metadata = {
  title: {
    default: "Floua - Beta",
    template: "%s | Floua - Beta"
  },
  description: "Designed for the next generation of creators - by Novus0x",
  icons: {
    icon: "/img/icon.svg",
  },
  keywords: ["Floua", "videos", "video platform", "no ads", "creators"]
};

/********************** Main **********************/
const RootLayout = ({ children }: { children: ReactNode }) => {

  return (
    <html>
      <head>
        <link rel="stylesheet" href="https://site-assets.fontawesome.com/releases/v6.7.2/css/all.css" />
        <link rel="stylesheet" href="https://site-assets.fontawesome.com/releases/v6.7.2/css/sharp-solid.css" />
        <link rel="stylesheet" href="https://site-assets.fontawesome.com/releases/v6.7.2/css/sharp-regular.css" />
        <link rel="stylesheet" href="https://site-assets.fontawesome.com/releases/v6.7.2/css/sharp-light.css" />
        <link rel="stylesheet" href="https://site-assets.fontawesome.com/releases/v6.7.2/css/duotone.css" />
        <link rel="stylesheet" href="https://site-assets.fontawesome.com/releases/v6.7.2/css/brands.css" />
      </head>

      <body>
        <UI_provider>
          <Notification_provider>
            <Navbar />
            <Sidebar />
            {children}
          </Notification_provider>
        </UI_provider>
      </body>
    </html>
  );
};

/********************** Export **********************/
export default RootLayout;
