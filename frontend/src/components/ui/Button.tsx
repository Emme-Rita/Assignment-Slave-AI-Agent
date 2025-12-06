import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'ghost';
}

export function Button({ className, variant = 'primary', ...props }: ButtonProps) {
    return (
        <button
            className={twMerge(
                clsx(
                    'inline-flex items-center justify-center px-4 py-2 rounded-lg font-medium transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-navy-900',
                    {
                        'btn-primary': variant === 'primary',
                        'bg-white/10 hover:bg-white/20 text-white': variant === 'secondary',
                        'hover:bg-white/5 text-gray-400 hover:text-white': variant === 'ghost',
                    },
                    className
                )
            )}
            {...props}
        />
    );
}
