import { Metadata } from "next";
import React from "react";
import { ComponentsOverview } from "@/app/dev/components";
import { ContentLayout } from "@/components/page-layout";

export const metadata: Metadata = {
  title: "UI component preview",
  description: "UI components",
};

export default async function ComponentsPage() {
  return (
    <ContentLayout layout="CenteredFeed">
      <ComponentsOverview />
    </ContentLayout>
  );
}
