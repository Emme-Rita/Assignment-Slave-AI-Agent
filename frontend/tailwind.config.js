/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                navy: {
                    900: '#020617', // Slate 950
                    800: '#0f172a', // Slate 900
                    700: '#1e293b', // Slate 800
                },
                primary: {
                    light: '#3b82f6', // Blue 500
                    DEFAULT: '#2563eb', // Blue 600
                    dark: '#1d4ed8', // Blue 700
                },
                success: {
                    light: '#34d399', // Emerald 400
                    DEFAULT: '#10b981', // Emerald 500
                    dark: '#059669', // Emerald 600
                },
                warning: {
                    light: '#fbbf24', // Amber 400
                    DEFAULT: '#f59e0b', // Amber 500
                    dark: '#d97706', // Amber 600
                },
                accent: {
                    purple: '#8b5cf6', // Violet 500
                    cyan: '#06b6d4', // Cyan 500
                    pink: '#ec4899', // Pink 500
                }
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            },
            borderRadius: {
                lg: 'var(--radius)',
                md: 'calc(var(--radius) - 2px)',
                sm: 'calc(var(--radius) - 4px)',
            },
            boxShadow: {
                'soft': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
                'glow': '0 0 15px rgba(37, 99, 235, 0.2)',
            },
            keyframes: {
                "accordion-down": {
                    from: { height: "0" },
                    to: { height: "var(--radix-accordion-content-height)" },
                },
                "accordion-up": {
                    from: { height: "var(--radix-accordion-content-height)" },
                    to: { height: "0" },
                },
            },
            animation: {
                "accordion-down": "accordion-down 0.2s ease-out",
                "accordion-up": "accordion-up 0.2s ease-out",
            },
        },
    },
    plugins: [],
}
