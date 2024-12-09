import type { Metadata } from "next";
import "./globals.css";
import { ReactNode } from "react";
import { License } from "@/components/licence";
import { Nav } from "@/components/nav";
import { TextLink } from "@/components/link";

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
      <body className="grid h-full grid-rows-[min-content_1fr_min-content] items-start bg-surface-100 text-surface-900 dark:bg-surface-800 dark:text-surface-50">
        <header className="flex w-full flex-col items-center gap-2 p-8">
          <h1>Commons</h1>
          <Nav>
            <TextLink href="/members/">Members</TextLink>
            <TextLink href="/parties/">Parties</TextLink>
            <TextLink href="/constituencies/">Constituencies</TextLink>
          </Nav>

          <Nav>
            <TextLink href="/admin/" target="_blank">
              admin
            </TextLink>
            <TextLink href="https://tailwindcss.com/docs/" target="_blank">
              tailwind docs
            </TextLink>
          </Nav>
        </header>

        <div className="grid w-full grid-cols-[1fr_minmax(300px,1350px)_1fr] items-center">
          <div id="side_left" />
          {children}
          <div id="side_right" />
        </div>

        <footer className="flex flex-col items-center gap-2 p-8 text-center">
          <License licence="OpenParliament" />
        </footer>
      </body>
    </html>
  );
}
