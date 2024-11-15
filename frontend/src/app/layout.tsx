import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";
import { ReactNode } from "react";

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
    <html lang="en">
      <body className="bg-white text-surface-900 dark:bg-surface-800 dark:text-surface-50">
        <header className="flex w-full flex-col items-center gap-2 p-8">
          <h1>Commons</h1>
          <nav className="flex gap-1 text-sm [&>a]:p-1 [&>a]:text-accent-900 dark:[&>a]:text-accent-200">
            <Link href="/members/">Members</Link>
            <Link href="/parties/">Parties</Link>
            <Link href="/constituencies/">Constituencies</Link>
          </nav>
        </header>

        <div className="grid grid-cols-[1fr_minmax(300px,1350px)_1fr] items-center">
          <div id="side_left" />
          {children}
          <div id="side_right" />
        </div>

        <footer className="bottom-0 flex w-full flex-row justify-center gap-2 p-8 [&>a]:p-4">
          <a href={"/admin/"} target="_blank">
            admin
          </a>
          <a href="https://tailwindcss.com/docs/" target="_blank">
            tailwind docs
          </a>
        </footer>
      </body>
    </html>
  );
}
