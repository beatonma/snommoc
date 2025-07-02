import { Metadata } from "next";
import React from "react";
import { ConstituencyList } from "@/app/constituencies/constituencies";
import { ContentLayout } from "@/components/page-layout";

export const metadata: Metadata = {
  title: "Constituencies",
  description: "Constituency list",
};

export default async function ConstituencyListPage() {
  return (
    <ContentLayout layout="CenteredFeed">
      <ConstituencyList />
    </ContentLayout>
  );
}
