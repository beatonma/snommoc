import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  trailingSlash: true,
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "members-api.parliament.uk",
      },
    ],
  },
};

export default nextConfig;
