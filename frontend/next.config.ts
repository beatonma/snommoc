import type { NextConfig } from "next";

const SERVER = process.env.SERVER;
const nextConfig: NextConfig = {
  output: "standalone",
  trailingSlash: true,
  async redirects() {
    return [
      {
        source: "/admin/",
        destination: `${SERVER}/admin/`,
        permanent: true,
      },
    ];
  },
  async rewrites() {
    return [
      {
        source: "/api/:path*/",
        destination: `${SERVER}/api/:path*/`,
      },
      {
        source: "/media/:path*",
        destination: `${SERVER}/media/:path*`,
      },
    ];
  },
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "members-api.parliament.uk",
      },
      {
        protocol: "https",
        hostname: "upload.wikimedia.org",
      },
    ],
  },
  turbopack: {
    rules: {
      "*.svg": {
        loaders: [
          {
            loader: "@svgr/webpack",
            options: {
              icon: true,
            },
          },
        ],
        as: "*.js",
      },
    },
  },
};

export default nextConfig;
