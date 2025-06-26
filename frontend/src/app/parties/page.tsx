import { Metadata } from "next";
import React from "react";
import { PartyList as PartyListPage } from "@/app/parties/parties";
import { PageLayout } from "@/components/page-layout";

export const metadata: Metadata = {
  title: "Parties",
  description: "Party list",
};

export default async function Page() {
  return (
    <PageLayout layout="CenteredFeed">
      <PartyListPage />
    </PageLayout>
  );
}
