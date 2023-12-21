/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['BIZ UDPGothic', 'HiraKakuProN-W6', 'Noto Color Emoji', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

