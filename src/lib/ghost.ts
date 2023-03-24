import GhostContentAPI from "@tryghost/content-api";
import type { GhostAPI } from "@tryghost/content-api";

// Create API instance with site credentials
export const ghostClient: GhostAPI = new GhostContentAPI({
  url: "http://blog.joshthomas.dev", // This is the default URL if your site is running on a local environment
  key: import.meta.env.CONTENT_API_KEY,
  version: "v5.0",
});
