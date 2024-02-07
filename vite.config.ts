import { resolve, basename } from "path";
import { readdirSync } from "fs";
import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import sveltePreprocess from "svelte-preprocess";

// https://vitejs.dev/config/
export default defineConfig({
  base: "/static/",
  build: {
    assetsDir: "",
    manifest: true,
    outDir: resolve(__dirname, "./static/dist"),
    rollupOptions: {
      input: readdirSync(resolve(__dirname, "./static/src/entrypoints")).reduce(
        (entries, file) => {
          const fileTypes = [".js", ".svelte", ".ts"];

          if (fileTypes.some((ext) => file.endsWith(ext))) {
            const name = basename(
              file,
              fileTypes.find((ext) => file.endsWith(ext)),
            );
            entries[name] = resolve(
              __dirname,
              "./static/src/entrypoints",
              file,
            );
          }
          return entries;
        },
        {},
      ),
      output: {
        chunkFileNames: undefined,
      },
    },
  },
  plugins: [
    svelte({
      preprocess: [sveltePreprocess({ typescript: true })],
    }),
  ],
  publicDir: "",
  resolve: {
    alias: {
      "@": resolve(__dirname, "./static/src"),
    },
    extensions: [".js", ".jsx", ".json", ".svelte", ".ts", ".tsx"],
  },
  root: resolve(__dirname, "./static/src/entrypoints"),
  server: {
    host: "127.0.0.1",
    port: 5173,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
});
