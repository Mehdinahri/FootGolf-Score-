import { z } from "zod";

const envSchema = z.object({
  NEXT_PUBLIC_API_URL: z.string().url("NEXT_PUBLIC_API_URL doit être une URL valide"),
  NEXT_PUBLIC_WS_URL: z.string().url("NEXT_PUBLIC_WS_URL doit être une URL valide"),
  NEXT_PUBLIC_APP_NAME: z.string().optional().default("FootGolf Score"),
});

// Process.env is not entirely available in the browser side safely unless prefixed with NEXT_PUBLIC
const envVars = {
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  NEXT_PUBLIC_WS_URL: process.env.NEXT_PUBLIC_WS_URL,
  NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME,
};

const parsedEnv = envSchema.safeParse(envVars);

if (!parsedEnv.success) {
  console.error("❌ Variables d'environnement invalides :", parsedEnv.error.format());
  throw new Error("Variables d'environnement invalides ou manquantes");
}

export const env = parsedEnv.data;
