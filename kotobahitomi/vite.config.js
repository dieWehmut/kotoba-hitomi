import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@assets": path.resolve(__dirname, "./src/assets"),
    },
  },
  //base: "/kotobahitomi/",
  //base:"./",
  base: "/testCase/",
  optimizeDeps: {
    include: ["**/*.json"],
  },
  build: {
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("node_modules")) {
            if (id.includes("pdfjs-dist")) return "pdfjs";
            if (id.includes("vue")) return "vue";
            return "vendor";
          }
        },
        assetFileNames: (assetInfo) => {
          if (assetInfo.name && assetInfo.name.includes("pdf.worker")) {
            // 自定义 worker 文件名输出，单独 chunk
            return "assets/pdf-worker-[hash][extname]";
          }
          return "assets/[name]-[hash][extname]";
        },
      },
    },
  },
});
