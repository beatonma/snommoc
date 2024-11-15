import React from "react";
import { Metadata } from "next";
import MembersList from "@/app/members/[parliamentdotuk]/members";

export const metadata: Metadata = {
  title: "Members",
  description: "Members list",
};

export default async function Page() {
  return (
    <main>
      <MembersList />
    </main>
  );
}
