import * as path from "node:path";

import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  /** Трейсинг файлов до корня репо (workspace) — для корректного standalone-артефакта */
  outputFileTracingRoot: path.join(__dirname, ".."),
};

export default nextConfig;
