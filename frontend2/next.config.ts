import type { NextConfig } from "next";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  // Django's API routes all end in "/" (APPEND_SLASH). Next.js would otherwise
  // redirect "/api/x/" to "/api/x" before proxying, which Django answers with a
  // 500 for POST requests (login, signup, saving data) and a redirect for GETs.
  skipTrailingSlashRedirect: true,
  async rewrites() {
    return [
      {
        // ":path*" never includes the trailing slash, so always add it back.
        source: '/api/:path*',
        destination: `${BACKEND_URL}/en/api/:path*/`,
      },
    ];
  },
};

export default nextConfig;
