/** @type {import('next').NextConfig} */
const nextConfig = {
  // TODO: Add image domains for article thumbnails
  // images: {
  //   domains: ["techcrunch.com", "bbc.co.uk", "reuters.com"],
  // },

  // API rewrites — proxy /api calls to the FastAPI backend in development
  async rewrites() {
    return [
      // TODO: Uncomment for local dev without Docker
      // {
      //   source: "/api/:path*",
      //   destination: "http://localhost:8000/api/:path*",
      // },
    ];
  },
};

module.exports = nextConfig;
