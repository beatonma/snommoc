import type { Metadata } from "next";
import { ReactNode } from "react";
import "./_style/index.css";

export const metadata: Metadata = {
  title: { default: "Commons", template: "%s - Commons" },
  description: "A client for browsing UK Parliament data",
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
