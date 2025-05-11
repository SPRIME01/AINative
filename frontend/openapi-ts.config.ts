import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "http://localhost:8000/openapi.json", // URL or path to your backend's OpenAPI schema
  output: {
    path: "./src/services/api/client", // Output directory for the generated client
    format: "prettier", // Format the generated code using Prettier
    client: "axios", // Generate an Axios client (since you have it as a dependency)
  },
  schemas: {
    type: "json", // Generate JSON schemas
  },
  services: {
    asClass: true, // Generate services as classes
  },
});
