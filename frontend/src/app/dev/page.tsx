import { Metadata } from "next";

import React from "react";
import { ComponentsOverview } from "@/app/dev/components";
import PageContent from "@/components/page";

export const metadata: Metadata = {
  title: "UI component preview",
  description: "UI components",
};

export default async function Page() {
  return (
    <PageContent>
      <main className="readable">
        <ComponentsOverview />
      </main>
    </PageContent>
  );
}
