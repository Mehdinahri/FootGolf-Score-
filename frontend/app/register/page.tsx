"use client";

import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useAuth } from "@/components/auth/AuthContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";
import Link from "next/link";

const registerSchema = z.object({
  first_name: z.string().min(1, "Prénom requis").max(100, "Trop long"),
  last_name: z.string().min(1, "Nom de famille requis").max(100, "Trop long"),
  email: z.string().email("Adresse email invalide"),
  password: z.string().min(8, "Le mot de passe doit contenir au moins 8 caractères"),
  captcha_answer: z.string().min(1, "Veuillez répondre au test robot"),
});

type RegisterForm = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const { login, user, isLoading } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const [captcha, setCaptcha] = useState({ a: 1, b: 1 });

  useEffect(() => {
    // Éviter les erreurs d'hydratation en générant les nombres uniquement côté client
    setCaptcha({
      a: Math.floor(Math.random() * 10) + 1,
      b: Math.floor(Math.random() * 10) + 1,
    });
  }, []);

  useEffect(() => {
    if (!isLoading && user) {
      router.push("/dashboard");
    }
  }, [user, isLoading, router]);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    resetField,
  } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterForm) => {
    try {
      setError(null);
      
      // Vérification du captcha
      const answer = parseInt(data.captcha_answer, 10);
      if (answer !== captcha.a + captcha.b) {
        setError("Réponse au test robot incorrecte. Veuillez réessayer.");
        setCaptcha({
          a: Math.floor(Math.random() * 10) + 1,
          b: Math.floor(Math.random() * 10) + 1,
        });
        resetField("captcha_answer");
        return;
      }

      // Envoi à l'API
      const payload = {
        first_name: data.first_name,
        last_name: data.last_name,
        email: data.email,
        password: data.password,
      };

      const res = await api.post("/auth/register", payload);
      const { access_token, refresh_token } = res.data.data;
      
      // Connexion automatique après inscription réussie
      login(access_token, refresh_token);
      window.location.href = "/dashboard";
    } catch (err: any) {
      if (err.response?.data?.message) {
        setError(err.response.data.message);
      } else {
        setError("Erreur de connexion au serveur. Le serveur est-il bien lancé ?");
      }
    }
  };

  return (
    <div className="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-sm">
        <h2 className="mt-10 text-center text-3xl font-bold tracking-tight text-slate-900">
          Créer un compte
        </h2>
        <p className="mt-2 text-center text-sm text-slate-600">
          Inscrivez-vous pour rejoindre les parties de FootGolf
        </p>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="first_name">Prénom</Label>
              <div className="mt-2">
                <Input
                  id="first_name"
                  type="text"
                  autoComplete="given-name"
                  {...register("first_name")}
                />
                {errors.first_name && (
                  <p className="mt-1 text-sm text-red-600">{errors.first_name.message}</p>
                )}
              </div>
            </div>
            <div>
              <Label htmlFor="last_name">Nom</Label>
              <div className="mt-2">
                <Input
                  id="last_name"
                  type="text"
                  autoComplete="family-name"
                  {...register("last_name")}
                />
                {errors.last_name && (
                  <p className="mt-1 text-sm text-red-600">{errors.last_name.message}</p>
                )}
              </div>
            </div>
          </div>

          <div>
            <Label htmlFor="email">Adresse Email</Label>
            <div className="mt-2">
              <Input
                id="email"
                type="email"
                autoComplete="email"
                {...register("email")}
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
              )}
            </div>
          </div>

          <div>
            <Label htmlFor="password">Mot de passe</Label>
            <div className="mt-2">
              <Input
                id="password"
                type="password"
                autoComplete="new-password"
                {...register("password")}
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
              )}
            </div>
          </div>

          <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg">
            <Label htmlFor="captcha_answer" className="flex items-center gap-2">
              🤖 Vérification anti-robot
            </Label>
            <p className="text-sm text-slate-600 mb-3 mt-1">
              Combien font <strong>{captcha.a} + {captcha.b}</strong> ?
            </p>
            <Input
              id="captcha_answer"
              type="number"
              placeholder="Votre réponse"
              {...register("captcha_answer")}
            />
            {errors.captcha_answer && (
              <p className="mt-1 text-sm text-red-600">{errors.captcha_answer.message}</p>
            )}
          </div>

          {error && (
            <div className="rounded-md bg-red-50 p-4 border border-red-100">
              <div className="flex">
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">{error}</h3>
                </div>
              </div>
            </div>
          )}

          <div>
            <Button
              type="submit"
              className="w-full bg-green-600 hover:bg-green-700 focus-visible:ring-green-500"
              disabled={isSubmitting}
            >
              {isSubmitting ? "Création en cours..." : "S'inscrire"}
            </Button>
          </div>
          
          <div className="mt-4 text-center text-sm">
            Vous avez déjà un compte ?{" "}
            <Link href="/login" className="font-semibold text-green-600 hover:text-green-500">
              Se connecter
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
