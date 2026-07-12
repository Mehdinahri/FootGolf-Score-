import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Providers from "./providers";
import { InstallPrompt } from "@/components/pwa/InstallPrompt";
import { ServiceWorkerRegister } from "@/components/pwa/ServiceWorkerRegister";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const viewport: Viewport = {
  themeColor: "#16a34a",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

export const metadata: Metadata = {
  title: "FootGolf Score",
  description: "Application de gestion des parties et des scores de FootGolf",
  manifest: "/manifest.webmanifest",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "FootGolf Score",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr" className="h-full">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased h-full flex flex-col bg-slate-50`}
      >
        <Providers>
          <ServiceWorkerRegister />
          {children}
          <InstallPrompt />
        </Providers>
      </body>
    </html>
  );
}
