import { Metadata } from "next";
import React from "react";
import { PartyList } from "@/app/parties/parties";
import { ContentLayout } from "@/components/page-layout";

export const metadata: Metadata = {
  title: "Parties",
  description: "Party list",
};

export default async function PartyListPage() {
  return (
    <ContentLayout layout="CenteredFeed">
      <PartyList />
    </ContentLayout>
  );
}
