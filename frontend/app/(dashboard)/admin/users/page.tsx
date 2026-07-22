"use client";

import { useQuery } from "@tanstack/react-query";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { userService } from "@/services/userService";
import { queryKeys } from "@/lib/queryKeys";
import { UserRole } from "@/types/domain/user";

export default function AdminUsersPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["users", "admin", "list"],
    queryFn: () => userService.getUsers(1, 50),
  });

  const users = data?.items || [];

  return (
    <ProtectedRoute adminOnly>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-slate-900">Utilisateurs</h1>
        </div>

        <div className="rounded-lg border border-slate-200 bg-white shadow-sm overflow-hidden overflow-x-auto">
          {isLoading ? (
            <div className="p-8 text-center text-slate-500">Chargement...</div>
          ) : (
            <table className="w-full text-sm text-left">
              <thead className="bg-slate-50 text-slate-500 border-b border-slate-200">
                <tr>
                  <th className="px-6 py-3 font-medium">Nom complet</th>
                  <th className="px-6 py-3 font-medium">Email</th>
                  <th className="px-6 py-3 font-medium">Rôle</th>
                  <th className="px-6 py-3 font-medium">Statut</th>
                  <th className="px-6 py-3 font-medium">Date de création</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {users.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-8 text-center text-slate-500">
                      Aucun utilisateur trouvé.
                    </td>
                  </tr>
                ) : (
                  users.map((user) => (
                    <tr key={user.id} className="hover:bg-slate-50/50">
                      <td className="px-6 py-4 font-medium text-slate-900">
                        {user.first_name} {user.last_name}
                      </td>
                      <td className="px-6 py-4 text-slate-500">{user.email}</td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ring-inset ${
                          user.role === "ADMIN" ? "bg-purple-50 text-purple-700 ring-purple-600/20" : 
                          user.role === "MARKER" ? "bg-blue-50 text-blue-700 ring-blue-600/20" : 
                          "bg-slate-50 text-slate-700 ring-slate-600/20"
                        }`}>
                          {user.role}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ring-inset ${
                          user.is_active ? "bg-green-50 text-green-700 ring-green-600/20" : "bg-red-50 text-red-700 ring-red-600/20"
                        }`}>
                          {user.is_active ? "Actif" : "Inactif"}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-slate-500 text-sm">
                        {user.created_at ? new Date(user.created_at).toLocaleDateString("fr-FR") : "-"}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
}
