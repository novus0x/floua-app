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
import { Auth_provider } from "@/context/auth";
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
      </head>

      <body>
        <Auth_provider>
          <UI_provider>
            <Notification_provider>
              <Navbar />
              <Sidebar />
              {children}
            </Notification_provider>
          </UI_provider>
        </Auth_provider>
      </body>
    </html>
  );
};

/********************** Export **********************/
export default RootLayout;
