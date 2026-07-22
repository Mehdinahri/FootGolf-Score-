"use client";

import { useState } from "react";
import { useCourses } from "@/hooks/queries/useCourses";
import { courseService } from "@/services/courseService";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Plus, Map, Flag, Info, X, Settings } from "lucide-react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { queryKeys } from "@/lib/queryKeys";

export default function AdminCoursesPage() {
  const [isCreating, setIsCreating] = useState(false);
  const [configuringCourseId, setConfiguringCourseId] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    name: "",
    city: "",
    hole_count: 18,
    par_total: 54,
    distance_total: 0,
  });
  const [holesData, setHolesData] = useState<Array<{ hole_number: number; par: number; distance: number; description: string; difficulty: number }>>([]);
  const [formError, setFormError] = useState<string | null>(null);

  const queryClient = useQueryClient();
  const { data: paginatedData, isLoading, error } = useCourses();
  const courses = paginatedData?.items;

  const createMutation = useMutation({
    mutationFn: () => courseService.createCourse(formData as any),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.courses.all });
      setIsCreating(false);
      setFormData({ name: "", city: "", hole_count: 18, par_total: 54, distance_total: 0 });
      setFormError(null);
    },
    onError: (err: any) => {
      setFormError(err?.response?.data?.message || "Erreur lors de la création du parcours");
    },
  });

  const saveHolesMutation = useMutation({
    mutationFn: (courseId: string) =>
      courseService.bulkSaveHoles(courseId, { holes: holesData } as any),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.courses.all });
      setConfiguringCourseId(null);
      setHolesData([]);
    },
    onError: (err: any) => {
      setFormError(err?.response?.data?.message || "Erreur lors de la sauvegarde des trous");
    },
  });

  const handleCreateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name) {
      setFormError("Le nom du parcours est obligatoire");
      return;
    }
    createMutation.mutate();
  };

  const openHolesConfig = (courseId: string) => {
    setConfiguringCourseId(courseId);
    setFormError(null);
    // Initialize 18 holes with defaults
    const defaultHoles = Array.from({ length: 18 }, (_, i) => ({
      hole_number: i + 1,
      par: 3,
      distance: 50,
      description: "",
      difficulty: 1,
    }));
    setHolesData(defaultHoles);
  };

  const updateHole = (index: number, field: string, value: number | string) => {
    setHolesData((prev) =>
      prev.map((h, i) => (i === index ? { ...h, [field]: value } : h))
    );
  };

  return (
    <ProtectedRoute adminOnly>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Gestion des Parcours
          </h1>
          <Button
            className="bg-green-600 hover:bg-green-700"
            onClick={() => setIsCreating(true)}
          >
            <Plus className="mr-2 h-5 w-5" />
            Nouveau Parcours
          </Button>
        </div>

        {/* Create Course Modal */}
        {isCreating && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
            <div className="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
              <div className="flex items-center justify-between p-6 border-b border-slate-200">
                <h2 className="text-lg font-bold text-slate-900">Nouveau Parcours</h2>
                <button
                  onClick={() => { setIsCreating(false); setFormError(null); }}
                  className="p-1 rounded-md text-slate-400 hover:text-slate-600"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              <form onSubmit={handleCreateSubmit} className="p-6 space-y-4">
                <div>
                  <Label htmlFor="name">Nom du parcours *</Label>
                  <Input
                    id="name"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    placeholder="Ex: Parcours du Lac"
                    className="mt-1"
                  />
                </div>
                <div>
                  <Label htmlFor="city">Ville</Label>
                  <Input
                    id="city"
                    value={formData.city}
                    onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                    placeholder="Ex: Paris"
                    className="mt-1"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="par_total">Par total</Label>
                    <Input
                      id="par_total"
                      type="number"
                      value={formData.par_total}
                      onChange={(e) => setFormData({ ...formData, par_total: parseInt(e.target.value) || 54 })}
                      className="mt-1"
                    />
                  </div>
                  <div>
                    <Label htmlFor="distance_total">Distance totale (m)</Label>
                    <Input
                      id="distance_total"
                      type="number"
                      value={formData.distance_total}
                      onChange={(e) => setFormData({ ...formData, distance_total: parseInt(e.target.value) || 0 })}
                      className="mt-1"
                    />
                  </div>
                </div>

                {formError && (
                  <div className="p-3 rounded-md bg-red-50 text-sm text-red-800 border border-red-200">
                    {formError}
                  </div>
                )}

                <div className="flex gap-3 pt-2">
                  <Button
                    type="button"
                    variant="outline"
                    className="flex-1"
                    onClick={() => { setIsCreating(false); setFormError(null); }}
                  >
                    Annuler
                  </Button>
                  <Button
                    type="submit"
                    className="flex-1 bg-green-600 hover:bg-green-700"
                    disabled={createMutation.isPending}
                  >
                    {createMutation.isPending ? "Création..." : "Créer le parcours"}
                  </Button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Configure Holes Modal */}
        {configuringCourseId && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
            <div className="bg-white rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
              <div className="flex items-center justify-between p-6 border-b border-slate-200">
                <h2 className="text-lg font-bold text-slate-900">Configurer les 18 trous</h2>
                <button
                  onClick={() => { setConfiguringCourseId(null); setFormError(null); }}
                  className="p-1 rounded-md text-slate-400 hover:text-slate-600"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              <div className="overflow-y-auto flex-1 p-6">
                <div className="space-y-3">
                  <div className="grid grid-cols-[60px_1fr_1fr_1fr] gap-2 text-xs font-semibold text-slate-500 uppercase px-1">
                    <span>Trou</span>
                    <span>Par</span>
                    <span>Distance (m)</span>
                    <span>Difficulté</span>
                  </div>
                  {holesData.map((hole, idx) => (
                    <div key={hole.hole_number} className="grid grid-cols-[60px_1fr_1fr_1fr] gap-2 items-center">
                      <span className="text-sm font-bold text-slate-700 text-center bg-slate-100 rounded-md py-2">
                        {hole.hole_number}
                      </span>
                      <Input
                        type="number"
                        min={1}
                        max={6}
                        value={hole.par}
                        onChange={(e) => updateHole(idx, "par", parseInt(e.target.value) || 3)}
                      />
                      <Input
                        type="number"
                        min={10}
                        max={300}
                        value={hole.distance}
                        onChange={(e) => updateHole(idx, "distance", parseInt(e.target.value) || 50)}
                      />
                      <select
                        value={hole.difficulty}
                        onChange={(e) => updateHole(idx, "difficulty", parseInt(e.target.value))}
                        className="block w-full rounded-md border border-slate-200 bg-white px-2 py-2 text-sm"
                      >
                        <option value={1}>Facile</option>
                        <option value={2}>Moyen</option>
                        <option value={3}>Difficile</option>
                      </select>
                    </div>
                  ))}
                </div>

                {formError && (
                  <div className="mt-4 p-3 rounded-md bg-red-50 text-sm text-red-800 border border-red-200">
                    {formError}
                  </div>
                )}
              </div>
              <div className="p-6 border-t border-slate-200 flex gap-3">
                <Button
                  variant="outline"
                  className="flex-1"
                  onClick={() => { setConfiguringCourseId(null); setFormError(null); }}
                >
                  Annuler
                </Button>
                <Button
                  className="flex-1 bg-green-600 hover:bg-green-700"
                  onClick={() => saveHolesMutation.mutate(configuringCourseId)}
                  disabled={saveHolesMutation.isPending}
                >
                  {saveHolesMutation.isPending ? "Sauvegarde..." : "Sauvegarder les trous"}
                </Button>
              </div>
            </div>
          </div>
        )}

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
            {courses?.length === 0 && (
              <div className="col-span-full rounded-lg border border-slate-200 bg-white p-12 text-center">
                <Map className="mx-auto h-12 w-12 text-slate-400" />
                <h3 className="mt-2 text-sm font-semibold text-slate-900">Aucun parcours</h3>
                <p className="mt-1 text-sm text-slate-500">
                  Cliquez sur "Nouveau Parcours" pour en créer un.
                </p>
              </div>
            )}
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
                  <Button
                    variant="outline"
                    className="w-full bg-white"
                    onClick={() => openHolesConfig(course.id)}
                  >
                    <Settings className="mr-2 h-4 w-4" />
                    Configurer les trous
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
