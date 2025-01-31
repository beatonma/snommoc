import type { Metadata } from "next";
import "./globals.css";
import { ReactNode } from "react";
import { License } from "@/components/licence";
import { Nav } from "@/components/nav";
import { TextLink } from "@/components/link";
import ThemeController from "@/components/themed/light-dark";

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
      <body className="bg-background text-on_background grid h-full grid-rows-[min-content_1fr_min-content] items-start">
        <header className="flex w-full flex-col items-center gap-2 p-8">
          <div className="grid w-full grid-cols-[1fr_max-content_1fr]">
            <div />
            <h1>Commons</h1>
            <div className="flex flex-row justify-end">
              <ThemeController className="sm:p-4" />
            </div>
          </div>
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

        <div className="grid w-full grid-cols-[1fr_minmax(auto,1350px)_1fr]">
          <div id="side_left" />
          {children}
          <div id="side_right" />
        </div>

        <footer className="flex flex-col items-center gap-2 p-8 pt-16 text-center">
          <License licence="OpenParliament" />
        </footer>

        {/*<script type="application/javascript">*/}
        {/*  window.addEventListener("load", () => { document.body.dataset.theme = window.localStorage.getItem("theme"); })*/}
        {/*</script>*/}
      </body>
    </html>
  );
}
