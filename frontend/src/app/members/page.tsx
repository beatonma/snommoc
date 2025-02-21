import React from "react";
import { Metadata } from "next";
import MembersList from "@/app/members/members";
import PageLayout from "@/components/page";

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
