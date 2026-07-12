"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";

export function InstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null);
  const [showPrompt, setShowPrompt] = useState(false);

  useEffect(() => {
    const handler = (e: any) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setShowPrompt(true);
    };

    window.addEventListener("beforeinstallprompt", handler);

    return () => {
      window.removeEventListener("beforeinstallprompt", handler);
    };
  }, []);

  const handleInstallClick = async () => {
    if (!deferredPrompt) return;

    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    
    if (outcome === "accepted") {
      setShowPrompt(false);
    }
    setDeferredPrompt(null);
  };

  if (!showPrompt) return null;

  return (
    <div className="fixed bottom-4 left-4 right-4 z-50 rounded-xl bg-white p-4 shadow-xl border border-slate-200 flex flex-col gap-3 sm:left-auto sm:w-96">
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-green-100 text-green-600">
          <Download className="h-5 w-5" />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-slate-900">Installer l'application</h3>
          <p className="text-xs text-slate-500 mt-1">
            Installez FootGolf Score pour une expérience plus rapide et un accès hors-ligne.
          </p>
        </div>
      </div>
      <div className="flex justify-end gap-2 mt-2">
        <Button variant="outline" size="sm" onClick={() => setShowPrompt(false)}>
          Plus tard
        </Button>
        <Button size="sm" className="bg-green-600 hover:bg-green-700" onClick={handleInstallClick}>
          Installer
        </Button>
      </div>
    </div>
  );
}
