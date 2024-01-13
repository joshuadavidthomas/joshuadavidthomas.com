const defaultColors = require("tailwindcss/colors");
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
    throw new Error(
      `Django management command exited with code ${result.status}`,
    );
  }

  return result.stdout
    .toString()
    .split("\n")
    .map((file) => file.trim())
    .filter(function(e) {
      return e;
    });
};

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./core/markdown.py",
    "./templates/**/*.svg",
  ].concat(getTemplateFiles()),
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
    },
  },
  plugins: [
    require("@tailwindcss/aspect-ratio"),
    require("@tailwindcss/container-queries"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("tailwindcss-debug-screens"),
    plugin(function({ addVariant }) {
      addVariant("htmx-settling", ["&.htmx-settling", ".htmx-settling &"]);
      addVariant("htmx-request", ["&.htmx-request", ".htmx-request &"]);
      addVariant("htmx-swapping", ["&.htmx-swapping", ".htmx-swapping &"]);
      addVariant("htmx-added", ["&.htmx-added", ".htmx-added &"]);
    }),
    plugin(function({ addComponents, theme }) {
      addComponents({
        ".prose .admonition": {
          borderRadius: theme("borderRadius.md"),
          borderWidth: theme("borderWidth.2"),
          paddingLeft: theme("spacing.4"),
          paddingRight: theme("spacing.4"),
          paddingTop: theme("spacing.2"),
          paddingBottom: theme("spacing.2"),
          fontSize: theme("fontSize.sm"),
          marginLeft: theme("spacing.2"),
          marginRight: theme("spacing.2"),
          marginBottom: theme("spacing.4"),
          backgroundColor: theme("colors.blue.50"),
          borderColor: theme("colors.blue.200"),
          color: theme("colors.blue.900"),
          "@media (prefers-color-scheme: dark)": {
            backgroundColor: theme("colors.blue.950"),
            borderColor: theme("colors.blue.900"),
            color: theme("colors.blue.100"),
          },
        },
        ".prose .admonition > *": {
          marginLeft: theme("spacing.4"),
        },
        ".prose .admonition-title": {
          fontWeight: theme("fontWeight.bold"),
          textTransform: "uppercase",
        },
        ".prose .admonition.tip": {
          backgroundColor: theme("colors.green.50"),
          borderColor: theme("colors.green.200"),
          color: theme("colors.green.900"),
          "@media (prefers-color-scheme: dark)": {
            backgroundColor: theme("colors.green.950"),
            borderColor: theme("colors.green.900"),
            color: theme("colors.green.100"),
          },
        },
        ".prose .admonition.info": {
          backgroundColor: theme("colors.gray.100"),
          borderColor: theme("colors.gray.200"),
          color: theme("colors.gray.900"),
          "@media (prefers-color-scheme: dark)": {
            backgroundColor: theme("colors.gray.800"),
            borderColor: theme("colors.gray.700"),
            color: theme("colors.gray.100"),
          },
        },
        ".prose .admonition.caution": {
          backgroundColor: theme("colors.orange.50"),
          borderColor: theme("colors.orange.200"),
          color: theme("colors.orange.900"),
          "@media (prefers-color-scheme: dark)": {
            backgroundColor: theme("colors.orange.950"),
            borderColor: theme("colors.orange.900"),
            color: theme("colors.orange.100"),
          },
        },
        ".prose .admonition.danger": {
          backgroundColor: theme("colors.red.50"),
          borderColor: theme("colors.red.200"),
          color: theme("colors.red.900"),
          "@media (prefers-color-scheme: dark)": {
            backgroundColor: theme("colors.red.950"),
            borderColor: theme("colors.red.900"),
            color: theme("colors.red.100"),
          },
        },
        ".prose .admonition.warning": {
          backgroundColor: theme("colors.yellow.50"),
          borderColor: theme("colors.yellow.200"),
          color: theme("colors.yellow.900"),
          "@media (prefers-color-scheme: dark)": {
            backgroundColor: theme("colors.yellow.950"),
            borderColor: theme("colors.yellow.900"),
            color: theme("colors.yellow.100"),
          },
        },
      });
    }),
    plugin(function({ addComponents }) {
      addComponents({
        ".scrollbar-stable": {
          scrollbarGutter: "stable both-edges",
        },
      });
    }),
  ],
};
