import * as React from "react"
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs))
}

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
    variant?: "default" | "secondary" | "destructive" | "outline" | "success" | "warning";
}

function badgeVariants(variant: BadgeProps["variant"]) {
    const variants = {
        default: "border-transparent bg-primary text-white hover:bg-primary/80 shadow-sm shadow-primary/20",
        secondary: "border-transparent bg-navy-700 text-gray-200 hover:bg-navy-700/80",
        destructive: "border-transparent bg-red-500/20 text-red-400 border border-red-500/30",
        success: "border-transparent bg-success/20 text-success-light border border-success/30",
        warning: "border-transparent bg-warning/20 text-warning-light border border-warning/30",
        outline: "text-gray-300 border-white/10",
    };
    return variants[variant || "default"];
}

function Badge({ className, variant, ...props }: BadgeProps) {
    return (
        <div
            className={cn(
                "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
                badgeVariants(variant),
                className
            )}
            {...props}
        />
    )
}

export { Badge }
