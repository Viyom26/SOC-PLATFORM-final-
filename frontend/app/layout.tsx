import "./globals.css";
import "../styles/layout.css";
import "@/styles/theme.css";

import ClientLayout from "@/components/ClientLayout";

export const metadata = {
  title: "AttackSurface SOC",
  description: "Enterprise SOC Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="transition-colors duration-300 bg-white text-gray-900 dark:bg-[#0b1220] dark:text-gray-100">
        <ClientLayout>{children}</ClientLayout>
      </body>
    </html>
  );
}