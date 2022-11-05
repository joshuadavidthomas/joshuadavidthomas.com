const colors = require("tailwindcss/colors");
const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  content: ["./src/**/*.{astro,ts,tsx}"],
  darkMode: "class",
  theme: {
    fontFamily: {
      mono: ["Fira Code", ...defaultTheme.fontFamily.mono],
    },
    extend: {
      colors: {
        gray: colors.zinc,
      },
    },
  },
  plugins: [
    require("@tailwindcss/aspect-ratio"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
  ],
};
