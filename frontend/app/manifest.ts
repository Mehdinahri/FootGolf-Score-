import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "FootGolf Score",
    short_name: "FootGolf",
    description: "Application de gestion des parties et des scores de FootGolf",
    start_url: "/dashboard",
    display: "standalone",
    background_color: "#f8fafc", // slate-50
    theme_color: "#16a34a", // green-600
    icons: [
      {
        src: "/icon-192x192.png",
        sizes: "192x192",
        type: "image/png",
      },
      {
        src: "/icon-512x512.png",
        sizes: "512x512",
        type: "image/png",
      },
    ],
  };
}
