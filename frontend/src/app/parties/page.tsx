import React from "react";
import { Metadata } from "next";
import PartyListPage from "@/app/parties/parties";
import PageLayout from "@/components/page";

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
