'use client';

/********************** Modules **********************/
import { useRouter } from "next/navigation";
import { use, useState, useEffect } from "react";

// DOM
import Link from "next/link";
import VideoCarousel from "@/components/actions/Video-Carousel"

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

  return (
    <div className="content">

      <VideoCarousel endpoint="/api/videos/newest" title="Newest" icon={ <GiElectric className="color-orange" size={40} /> } actions text="Watch more" url="#" />
    </div>
  );
};

export default Home;