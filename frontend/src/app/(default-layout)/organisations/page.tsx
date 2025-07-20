import { Metadata } from "next";
import React from "react";
import { OrganisationsList } from "@/app/(default-layout)/organisations/organisations";
import { ContentLayout } from "@/components/page-layout";

export const metadata: Metadata = {
  title: "Organisations",
  description: "Organisations list",
};

export default async function OrganisationsListPage() {
  return (
    <ContentLayout layout="CenteredFeed">
      <OrganisationsList />
    </ContentLayout>
  );
}
