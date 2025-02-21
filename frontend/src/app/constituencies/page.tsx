import React from "react";
import { Metadata } from "next";
import ConstituencyListPage from "@/app/constituencies/constituencies";
import PageLayout from "@/components/page";

export const metadata: Metadata = {
  title: "Constituencies",
  description: "Constituency list",
};

export default async function Page() {
  return (
    <PageLayout layout="CenteredFeed">
      <ConstituencyListPage />
    </PageLayout>
  );
}
