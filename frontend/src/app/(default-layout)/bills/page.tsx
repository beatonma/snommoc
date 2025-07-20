import { Metadata } from "next";
import React from "react";
import { BillsList } from "@/app/(default-layout)/bills/bills";
import { ContentLayout } from "@/components/page-layout";

export const metadata: Metadata = {
  title: "Bills",
  description: "Bills list",
};

export default async function MembersListPage() {
  return (
    <ContentLayout layout="CenteredFeed">
      <BillsList />
    </ContentLayout>
  );
}
