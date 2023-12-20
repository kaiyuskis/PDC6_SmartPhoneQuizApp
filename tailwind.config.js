/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['BIZ UDPGothic', 'Noto Color Emoji', 'HiraKakuProN-W6', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

