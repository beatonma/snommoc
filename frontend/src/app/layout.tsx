import type { Metadata } from "next";
import { ReactNode } from "react";
import { TextLink } from "@/components/link";
import { Nav } from "@/components/nav";
import ThemeController from "@/components/themed/light-dark";
import { License } from "./_components/licence";
import "./_style/globals.css";

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
      <body className="bg-background text-on_background grid h-full grid-cols-1 grid-rows-[min-content_1fr_min-content]">
        <header className="column items-center gap-x-2 p-8">
          <div className="grid w-full grid-cols-[1fr_max-content_1fr] items-center">
            <div />
            <h1>Commons</h1>
            <div className="row justify-end">
              <ThemeController className="p-2 sm:p-4" />
            </div>
          </div>
          <Nav>
            <TextLink href="/members/">Members</TextLink>
            <TextLink href="/parties/">Parties</TextLink>
            <TextLink href="/constituencies/">Constituencies</TextLink>
            <TextLink href="/maps/">Maps</TextLink>
          </Nav>

          <Nav>
            <TextLink href="/admin/" target="_blank">
              admin
            </TextLink>
            <TextLink href="https://tailwindcss.com/docs/" target="_blank">
              tailwind docs
            </TextLink>
            <TextLink href="/dev/" target="_blank">
              components
            </TextLink>
          </Nav>
        </header>

        {children}

        <footer className="column items-center gap-2 p-8 pt-16 text-center">
          <License licence="OpenParliament" />
        </footer>
      </body>
    </html>
  );
}
