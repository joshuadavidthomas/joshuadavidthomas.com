module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: ["airbnb", "eslint:recommended", "next/core-web-vitals"],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: module,
  },
  rules: {
    "import/extensions": [
      "error",
      "ignorePackages",
      {
        js: "never",
        jsx: "never",
        ts: "never",
        tsx: "never",
      },
    ],
  },
  overrides: [
    {
      files: ["**/*.ts?(x)"],
      parser: "@typescript-eslint/parser",
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
        ecmaVersion: 12,
        sourceType: module,
        project: "./tsconfig.json",
      },
      extends: ["airbnb-typescript", "plugin:react/recommended"],
      plugins: ["react", "@typescript-eslint"],
      rules: {
        "react/jsx-uses-react": "off",
        "react/react-in-jsx-scope": "off",
        "react/prop-types": "off",
        "react/require-default-props": "off",
      },
    },
  ],
};
