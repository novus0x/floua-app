'use client';

/********************** Modules **********************/
import { useRouter } from "next/navigation";
import { use, useState, useEffect } from "react";

// DOM
import Link from "next/link";
import VideoCarousel from "@/components/Video-Carousel"

// Icons
import { GiElectric } from "react-icons/gi";

// Auth
import { useAuth } from "@/context/auth";

// Routes
import { routes } from "@/helpers/routes";

// Notifications
import { useNotification } from "@/context/notifications";

// API
import { get_data } from "@/helpers/api";


/********************** Home **********************/
const Home = () => {
  // Auth
  const { user } = useAuth();

  // Router
  const router = useRouter();

  // Structures


  // States


  // Variables


  // Call API 


  return (
    <div className="content">

      <VideoCarousel endpoint="/api/videos/newest" title="Newest" icon={ <GiElectric className="color-orange" size={40} /> } />
    </div>
  );
};

export default Home;