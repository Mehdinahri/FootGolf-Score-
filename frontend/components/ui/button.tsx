import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cn } from "@/lib/utils"

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean
  variant?: "default" | "outline" | "ghost"
  size?: "default" | "sm" | "lg"
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    
    // Simple classes mapping
    const variantClasses = {
      default: "bg-slate-900 text-slate-50 shadow hover:bg-slate-900/90",
      outline: "border border-slate-200 bg-white hover:bg-slate-100 text-slate-900",
      ghost: "hover:bg-slate-100 hover:text-slate-900 text-slate-700",
    }
    
    const sizeClasses = {
      default: "h-12 px-8 py-2",
      sm: "h-9 rounded-md px-3 text-xs",
      lg: "h-14 rounded-md px-8 text-base",
    }
    return (
      <Comp
        className={cn(
          "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-slate-950 disabled:pointer-events-none disabled:opacity-50",
          variantClasses[variant],
          sizeClasses[size],
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button }
