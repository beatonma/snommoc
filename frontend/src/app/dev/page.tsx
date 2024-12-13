import { Metadata } from "next";

import React from "react";
import { ComponentsOverview } from "@/app/dev/components";

export const metadata: Metadata = {
  title: "UI component preview",
  description: "UI components",
};

export default async function Page() {
  return (
    <main>
      <ComponentsOverview />
    </main>
  );
}
