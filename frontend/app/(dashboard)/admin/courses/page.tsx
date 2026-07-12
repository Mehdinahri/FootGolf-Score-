"use client";


import { useCourses } from "@/hooks/queries/useCourses";
import { Button } from "@/components/ui/button";
import { Plus, Map, Flag, Info } from "lucide-react";

export default function AdminCoursesPage() {
  const { data: paginatedData, isLoading, error } = useCourses();
  const courses = paginatedData?.items;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Gestion des Parcours
        </h1>
        <Button className="bg-green-600 hover:bg-green-700">
          <Plus className="mr-2 h-5 w-5" />
          Nouveau Parcours
        </Button>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-12">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-green-600"></div>
        </div>
      ) : error ? (
        <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-6 text-center">
          <Info className="mx-auto h-12 w-12 text-yellow-400" />
          <h3 className="mt-2 text-sm font-semibold text-yellow-800">Section Admin Indisponible</h3>
          <p className="mt-1 text-sm text-yellow-600">
            L'API des parcours n'est pas encore implémentée côté serveur.
          </p>
        </div>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {courses?.map((course: any) => (
            <div key={course.id} className="rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden flex flex-col">
              <div className="p-5">
                <div className="flex items-center justify-between mb-4">
                  <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${course.is_active ? 'bg-green-50 text-green-700' : 'bg-slate-100 text-slate-700'}`}>
                    {course.is_active ? 'Actif' : 'Inactif'}
                  </span>
                  <div className="flex items-center text-sm font-bold text-slate-700">
                    <Flag className="mr-1 h-4 w-4" />
                    {course.hole_count} trous
                  </div>
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-1">{course.name}</h3>
                <p className="text-sm text-slate-500 flex items-center mb-4">
                  <Map className="mr-1.5 h-4 w-4" />
                  {course.city || "Lieu non défini"}
                </p>
                <div className="flex justify-between text-sm text-slate-600 border-t border-slate-100 pt-4">
                  <div>
                    <span className="block text-xs text-slate-400">Par Total</span>
                    <span className="font-semibold">{course.par_total}</span>
                  </div>
                  <div className="text-right">
                    <span className="block text-xs text-slate-400">Distance</span>
                    <span className="font-semibold">{course.distance_total} m</span>
                  </div>
                </div>
              </div>
              <div className="bg-slate-50 p-4 mt-auto border-t border-slate-100">
                <Button variant="outline" className="w-full bg-white">
                  Configurer les trous
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
