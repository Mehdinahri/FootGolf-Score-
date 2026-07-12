import { type ClassValue, clsx } from "clsx"
import { extendTailwindMerge } from "tailwind-merge"

const customTwMerge = extendTailwindMerge({
  extend: {
    theme: {
      colors: ["primary", "secondary", "destructive", "muted", "accent", "popover", "card"],
    },
  },
})

export function cn(...inputs: ClassValue[]) {
  return customTwMerge(clsx(inputs))
}
