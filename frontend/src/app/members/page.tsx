import { Metadata } from "next";
import React from "react";
import MembersList from "@/app/members/members";
import PageLayout from "@/components/page-layout";

export const metadata: Metadata = {
  title: "Members",
  description: "Members list",
};

export default async function Page() {
  return (
    <PageLayout layout="CenteredFeed">
      <MembersList />
    </PageLayout>
  );
}
