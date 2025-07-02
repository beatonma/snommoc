import { Metadata } from "next";
import React from "react";
import { MembersList } from "@/app/members/members";
import { ContentLayout } from "@/components/page-layout";

export const metadata: Metadata = {
  title: "Members",
  description: "Members list",
};

export default async function MembersListPage() {
  return (
    <ContentLayout layout="CenteredFeed">
      <MembersList />
    </ContentLayout>
  );
}
