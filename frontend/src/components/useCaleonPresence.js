import { useEffect, useState } from 'react';

export function useCaleonPresence() {
  const [status, setStatus] = useState("Ready");

  useEffect(() => {
    const phrases = [
      "Ready",
      "Active",
      "Monitoring",
      "Present",
      "Available",
      "Online",
      "Standing by",
      "Attentive",
      "Focused",
      "Engaged",
      "Connected",
      "Processing"
    ];

    const interval = setInterval(() => {
      const random = Math.random();
      if (random < 0.12) { // 12% chance every 15 seconds
        const newPhrase = phrases[Math.floor(Math.random() * phrases.length)];
        setStatus(newPhrase);
      }
    }, 15000);

    return () => clearInterval(interval);
  }, []);

  return status;
}