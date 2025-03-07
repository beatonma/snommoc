import type { Metadata } from "next";
import { ReactNode } from "react";
import GlobalFooter from "./_components/global-footer";
import GlobalHeader from "./_components/global-header";
import "./_style/globals.css";
import "./_style/root-layout.css";

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
      <body className="bg-background text-on_background">
        <GlobalHeader />

        <div className="global-content-wrapper">{children}</div>

        <GlobalFooter />
      </body>
    </html>
  );
}
