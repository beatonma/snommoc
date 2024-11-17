import React from "react";
import { Metadata } from "next";
import PartyListPage from "@/app/parties/parties";

export const metadata: Metadata = {
  title: "Parties",
  description: "Party list",
};

export default async function Page() {
  return <PartyListPage />;
}
