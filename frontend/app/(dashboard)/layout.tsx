"use client";

import { useAuth } from "@/components/auth/AuthContext";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { NetworkStatus } from "@/components/ui/NetworkStatus";
import { LogOut, Menu, UserCircle } from "lucide-react";
import Link from "next/link";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, logout } = useAuth();

  return (
    <ProtectedRoute>
      <div className="min-h-full flex flex-col">
        <NetworkStatus />
        {/* Navigation */}
        <nav className="bg-slate-900 border-b border-slate-800">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="flex h-16 justify-between">
              <div className="flex">
                <div className="flex flex-shrink-0 items-center">
                  <span className="text-white font-bold text-xl">FootGolf Score</span>
                </div>
                <div className="hidden sm:-my-px sm:ml-6 sm:flex sm:space-x-8">
                  <Link
                    href="/dashboard"
                    className="border-green-500 text-white inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium"
                  >
                    Tableau de bord
                  </Link>
                  {user?.role === "ADMIN" && (
                    <Link
                      href="/admin/games"
                      className="border-transparent text-slate-300 hover:border-slate-300 hover:text-white inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium"
                    >
                      Administration
                    </Link>
                  )}
                </div>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:items-center">
                <div className="flex items-center gap-3 text-sm text-slate-300">
                  <UserCircle className="h-5 w-5" />
                  <span>{user?.first_name} {user?.last_name}</span>
                </div>
                <button
                  onClick={logout}
                  className="ml-4 rounded-md bg-slate-800 p-2 text-slate-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-slate-800"
                >
                  <LogOut className="h-5 w-5" />
                </button>
              </div>
              
              {/* Mobile menu button */}
              <div className="-mr-2 flex items-center sm:hidden">
                <button className="inline-flex items-center justify-center rounded-md bg-slate-800 p-2 text-slate-400 hover:bg-slate-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-slate-800">
                  <span className="sr-only">Ouvrir le menu</span>
                  <Menu className="block h-6 w-6" aria-hidden="true" />
                </button>
              </div>
            </div>
          </div>
        </nav>

        {/* Content */}
        <main className="flex-1">
          <div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
