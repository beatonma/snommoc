import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";
import { ReactNode } from "react";
import { License } from "@/licensing";
import { Nav } from "@/components/nav";

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
    <html lang="en" className="h-full w-full">
      <body className="grid h-full grid-rows-[min-content_1fr_min-content] items-start bg-white text-surface-900 dark:bg-surface-800 dark:text-surface-50">
        <header className="flex w-full flex-col items-center gap-2 p-8">
          <h1>Commons</h1>
          <Nav>
            <Link href="/members/">Members</Link>
            <Link href="/parties/">Parties</Link>
            <Link href="/constituencies/">Constituencies</Link>
          </Nav>
        </header>

        <div className="grid grid-cols-[1fr_minmax(300px,1350px)_1fr] items-center">
          <div id="side_left" />
          {children}
          <div id="side_right" />
        </div>

        <footer className="flex flex-col items-center gap-2 p-8">
          <License licence="OpenParliament" />
          <Nav>
            <a href="/admin/" target="_blank">
              admin
            </a>
            <a href="https://tailwindcss.com/docs/" target="_blank">
              tailwind docs
            </a>
          </Nav>
        </footer>
      </body>
    </html>
  );
}
