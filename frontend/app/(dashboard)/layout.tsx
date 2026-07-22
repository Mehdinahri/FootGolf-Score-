"use client";

import { useState } from "react";
import { useAuth } from "@/components/auth/AuthContext";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { NetworkStatus } from "@/components/ui/NetworkStatus";
import { LogOut, Menu, X, UserCircle, LayoutDashboard, Settings, Map, Users } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const pathname = usePathname();

  const isAdmin = user?.role === "ADMIN";

  const navLinks = [
    { href: "/dashboard", label: "Tableau de bord", icon: LayoutDashboard },
    { href: "/profile", label: "Mon Profil", icon: UserCircle },
    ...(isAdmin
      ? [
          { href: "/admin/games", label: "Gestion Parties", icon: Settings },
          { href: "/admin/courses", label: "Gestion Parcours", icon: Map },
          { href: "/admin/users", label: "Utilisateurs", icon: Users },
        ]
      : []),
  ];

  const isActive = (href: string) => pathname === href;

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
                  {navLinks.map((link) => (
                    <Link
                      key={link.href}
                      href={link.href}
                      className={`inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium ${
                        isActive(link.href)
                          ? "border-green-500 text-white"
                          : "border-transparent text-slate-300 hover:border-slate-300 hover:text-white"
                      }`}
                    >
                      {link.label}
                    </Link>
                  ))}
                </div>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:items-center">
                <div className="flex items-center gap-3 text-sm text-slate-300">
                  <UserCircle className="h-5 w-5" />
                  <span>{user?.first_name} {user?.last_name}</span>
                  {isAdmin && (
                    <span className="ml-1 inline-flex items-center rounded-full bg-green-900/50 px-2 py-0.5 text-xs font-medium text-green-400 ring-1 ring-inset ring-green-400/30">
                      Admin
                    </span>
                  )}
                </div>
                <button
                  onClick={logout}
                  className="ml-4 rounded-md bg-slate-800 p-2 text-slate-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-slate-800"
                  title="Se déconnecter"
                >
                  <LogOut className="h-5 w-5" />
                </button>
              </div>
              
              {/* Mobile menu button */}
              <div className="-mr-2 flex items-center sm:hidden">
                <button
                  onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                  className="inline-flex items-center justify-center rounded-md bg-slate-800 p-2 text-slate-400 hover:bg-slate-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-slate-800"
                >
                  <span className="sr-only">
                    {mobileMenuOpen ? "Fermer le menu" : "Ouvrir le menu"}
                  </span>
                  {mobileMenuOpen ? (
                    <X className="block h-6 w-6" aria-hidden="true" />
                  ) : (
                    <Menu className="block h-6 w-6" aria-hidden="true" />
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Mobile menu panel */}
          {mobileMenuOpen && (
            <div className="sm:hidden border-t border-slate-800 bg-slate-900">
              <div className="space-y-1 px-2 pb-3 pt-2">
                {navLinks.map((link) => {
                  const Icon = link.icon;
                  return (
                    <Link
                      key={link.href}
                      href={link.href}
                      onClick={() => setMobileMenuOpen(false)}
                      className={`flex items-center gap-3 rounded-md px-3 py-2 text-base font-medium ${
                        isActive(link.href)
                          ? "bg-slate-800 text-white"
                          : "text-slate-300 hover:bg-slate-800 hover:text-white"
                      }`}
                    >
                      <Icon className="h-5 w-5" />
                      {link.label}
                    </Link>
                  );
                })}
              </div>
              <div className="border-t border-slate-800 pb-3 pt-4">
                <div className="flex items-center px-5">
                  <UserCircle className="h-8 w-8 text-slate-400" />
                  <div className="ml-3">
                    <div className="text-base font-medium text-white">
                      {user?.first_name} {user?.last_name}
                    </div>
                    <div className="text-sm font-medium text-slate-400">
                      {user?.email}
                    </div>
                  </div>
                </div>
                <div className="mt-3 space-y-1 px-2">
                  <button
                    onClick={() => {
                      setMobileMenuOpen(false);
                      logout();
                    }}
                    className="flex w-full items-center gap-3 rounded-md px-3 py-2 text-base font-medium text-slate-400 hover:bg-slate-800 hover:text-white"
                  >
                    <LogOut className="h-5 w-5" />
                    Se déconnecter
                  </button>
                </div>
              </div>
            </div>
          )}
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
