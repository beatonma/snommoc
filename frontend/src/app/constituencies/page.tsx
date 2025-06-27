import { Metadata } from "next";
import React from "react";
import { ConstituencyList } from "@/app/constituencies/constituencies";
import { PageLayout } from "@/components/page-layout";

export const metadata: Metadata = {
  title: "Constituencies",
  description: "Constituency list",
};

export default async function ConstituencyListPage() {
  return (
    <PageLayout layout="CenteredFeed">
      <ConstituencyList />
    </PageLayout>
  );
}
