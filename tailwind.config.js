/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
    "./**/*.js",
  ],
  theme: {
    extend: {
      fontFamily: {
        jersey: ["'Jersey 15'", "sans-serif"],
      },
    },
  },
  plugins: [],
}
