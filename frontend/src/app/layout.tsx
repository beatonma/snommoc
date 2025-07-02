import type { Metadata } from "next";
import { ReactNode } from "react";
import "./_style/index.css";

export const metadata: Metadata = {
  title: "Commons",
  description: "Commons browser",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en" className="h-full">
      {children}
    </html>
  );
}
