'use client';

/********************** Modules **********************/
import { useState, useEffect } from "react";

// DOM
import Link from "next/link";

// Routes
import { routes } from "@/helpers/routes";

// Auth
import { useAuth } from "@/context/auth";

// API
import { get_data, send_data } from "@/helpers/api";

/********************** Account **********************/
const Account = () => {
  // Auth
  const { user } = useAuth();

  // Help

  // States

  // Member since

  // API calls

  return (
    <div>
        <h3>IDK</h3>
    </div>
  );
};

export default Account;