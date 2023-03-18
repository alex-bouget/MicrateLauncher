/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: [
    './**/*.html',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      backgroundImage: {
        'background': "url('/src/img/background.png')",
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}