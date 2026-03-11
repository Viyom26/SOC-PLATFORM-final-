"use client";

import Link from "next/link";

export default function AuthCard({
  title,
  subtitle,
  children,
  footerText,
  footerLink,
  footerHref,
}: {
  title: string;
  subtitle: string;
  children: React.ReactNode;
  footerText: string;
  footerLink: string;
  footerHref: string;
}) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-black via-gray-900 to-black">
      <div className="w-full max-w-md bg-gray-900 border border-gray-800 rounded-xl shadow-xl p-8">
        
        {/* Logo */}
        <div className="text-center mb-6">
          <div className="mx-auto mb-3 h-12 w-12 rounded-full bg-red-600 flex items-center justify-center text-xl font-bold">
            🛡️
          </div>
          <h1 className="text-2xl font-bold text-white">
            AttackSurface SOC
          </h1>
          <p className="text-sm text-gray-400">
            Security Operations Center Platform
          </p>
        </div>

        {/* Title */}
        <h2 className="text-xl font-semibold text-white text-center">
          {title}
        </h2>
        <p className="text-gray-400 text-sm text-center mb-6">
          {subtitle}
        </p>

        {children}

        {/* Footer */}
        <p className="mt-6 text-center text-sm text-gray-400">
          {footerText}{" "}
          <Link href={footerHref} className="text-red-500 hover:underline">
            {footerLink}
          </Link>
        </p>
      </div>
    </div>
  );
}
