const defaultTheme = require("tailwindcss/defaultTheme");
const defaultColors = require("tailwindcss/colors");
const defaultTheme = require("tailwindcss/defaultTheme");
const plugin = require("tailwindcss/plugin");

// https://noumenal.es/notes/tailwind/django-integration/
// Resolve path to directory containing manage.py file.
// This is the root of the project.
// Then assumed layout of <main-app>/static/css/tailwind.config.js, so up 3 levels.
// Adjust for your needs.
const path = require("path");
const projectRoot = path.resolve(__dirname);

const { spawnSync } = require("child_process");

// Function to execute the Django management command and capture its output
const getTemplateFiles = () => {
  const command = "python"; // Requires virtualenv to be activated.
  const args = ["manage.py", "tailwind", "list_templates"]; // Requires cwd to be set.
  const options = { cwd: projectRoot };
  const result = spawnSync(command, args, options);

  if (result.error) {
    throw result.error;
  }

  if (result.status !== 0) {
    console.log(result.stdout.toString(), result.stderr.toString());
  }

  return result.stdout
    .toString()
    .split("\n")
    .map((file) => file.trim())
    .filter(function (e) {
      return e;
    });
};

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./core/markdown.py", "./templates/**/*.svg"].concat(
    getTemplateFiles(),
  ),
  theme: {
    extend: {
      colors: {
        gray: defaultColors.neutral,
        primary: defaultColors.indigo,
        secondary: defaultColors.gray,
        tertiary: defaultColors.green,
        aspect: defaultColors.orange,
        danger: defaultColors.red,
      },
      fontFamily: {
        brico: ["BricolageGrotesque", ...defaultTheme.fontFamily.sans],
        mono: ["MonoLisa", ...defaultTheme.fontFamily.mono],
        sans: ["InterVariable", ...defaultTheme.fontFamily.sans],
      },
      screens: {
        xs: "425px",
      },
    },
  },
  plugins: [
    require("@tailwindcss/aspect-ratio"),
    require("@tailwindcss/container-queries"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("tailwindcss-debug-screens"),
    plugin(function ({ addVariant }) {
      addVariant("htmx-settling", ["&.htmx-settling", ".htmx-settling &"]);
      addVariant("htmx-request", ["&.htmx-request", ".htmx-request &"]);
      addVariant("htmx-swapping", ["&.htmx-swapping", ".htmx-swapping &"]);
      addVariant("htmx-added", ["&.htmx-added", ".htmx-added &"]);
    }),
    plugin(function ({ addUtilities, theme }) {
      const widths = theme("maxWidth");
      const gridUtilities = {};
      Object.keys(widths).forEach((scale) => {
        gridUtilities[`.hg-grid-${scale}`] = {
          display: "grid",
          gridTemplateColumns: `1fr min(${widths[scale]}, 100%) 1fr`,
        };
        gridUtilities[`.hg-grid-${scale} > *`] = {
          gridColumn: "2",
        };
      });

      const newUtilities = {
        ".hg-grid": {
          display: "grid",
          gridTemplateColumns: "1fr min(65ch, 100%) 1fr",
        },
        ".hg-grid > *": {
          gridColumn: "2",
        },
        ...gridUtilities,
      };

      Object.keys(widths).forEach((size) => {
        newUtilities[`.stretch-to-${size}`] = {
          width: "100%",
          gridColumn: "1 / 4",
          maxWidth: widths[size],
          marginLeft: "auto",
          marginRight: "auto",
        };
      });

      addUtilities(newUtilities, ["responsive"]);
    }),
    plugin(function ({ addBase, theme }) {
      const colors = theme("colors");
      const colorVariables = {};

      Object.keys(colors).forEach((colorKey) => {
        const color = colors[colorKey];
        if (typeof color === "object") {
          Object.keys(color).forEach((shade) => {
            colorVariables[`--tw-color-${colorKey}-${shade}`] = color[shade];
          });
          colorVariables[`--tw-color-${colorKey}`] = color[500];
        } else {
          colorVariables[`--tw-color-${colorKey}`] = color;
        }
      });

      addBase({ ":root": colorVariables });
    }),
    plugin(function ({ addBase, theme }) {
      const colors = theme("colors");
      const colorVariables = {};

      Object.keys(colors).forEach((colorKey) => {
        const color = colors[colorKey];
        if (typeof color === "object") {
          Object.keys(color).forEach((shade) => {
            colorVariables[`--tw-color-${colorKey}-${shade}`] = color[shade];
          });
          colorVariables[`--tw-color-${colorKey}`] = color[500];
        } else {
          colorVariables[`--tw-color-${colorKey}`] = color;
        }
      });

      addBase({ ":root": colorVariables });
    }),
  ],
};
