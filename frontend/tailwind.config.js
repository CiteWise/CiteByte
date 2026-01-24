/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './pages/**/*.{js,ts,jsx,tsx,mdx}',
        './components/**/*.{js,ts,jsx,tsx,mdx}',
        './app/**/*.{js,ts,jsx,tsx,mdx}',
    ],
    theme: {
        extend: {
            colors: {
                'academic-blue': '#1e3a8a',
                'academic-navy': '#0f172a',
            },
            fontFamily: {
                serif: ['Georgia', 'Cambria', 'Times New Roman', 'serif'],
            },
        },
    },
    plugins: [],
}
