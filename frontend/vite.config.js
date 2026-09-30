import { resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";

const frontendRoot = fileURLToPath(new URL(".", import.meta.url));

export default defineConfig({
  server: {
    proxy: {
      "/tickets": process.env.API_PROXY_TARGET || "http://127.0.0.1:8000"
    }
  },
  build: {
    rollupOptions: {
      input: {
        index: resolve(frontendRoot, "index.html"),
        newTicket: resolve(frontendRoot, "new-ticket.html"),
        reviewTicket: resolve(frontendRoot, "review-ticket.html")
      }
    }
  }
});
