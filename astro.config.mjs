import { defineConfig } from "astro/config";

import tailwind from "@astrojs/tailwind";
import prefetch from "@astrojs/prefetch";
import vercel from "@astrojs/vercel/serverless";
import preact from "@astrojs/preact";

import { defaultLayoutPlugin } from "./src/plugins/defaultLayout";

// https://astro.build/config
export default defineConfig({
  integrations: [
    tailwind({
      config: {
        applyBaseStyles: false,
      },
    }),
    prefetch({
      throttle: 3,
    }),
    preact(),
  ],
  markdown: {
    remarkPlugins: [
      [
        defaultLayoutPlugin,
        [
          {
            dirname: "til",
            layout: "TIL.astro",
          },
        ],
      ],
    ],
  },
  output: "server",
  adapter: vercel(),
});
