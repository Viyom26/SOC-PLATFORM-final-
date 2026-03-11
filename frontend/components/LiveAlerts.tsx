"use client";

import { useEffect } from "react";

function fetchAlerts(): void {
  console.log("Fetching alerts...");
}

export default function LiveAlerts() {

  useEffect(() => {

    const interval = setInterval(fetchAlerts, 5000);

    return () => clearInterval(interval);

  }, []);

  return null;
}