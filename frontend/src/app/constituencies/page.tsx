import React from "react";
import { Metadata } from "next";
import ConstituencyListPage from "@/app/constituencies/constituencies";

export const metadata: Metadata = {
  title: "Parties",
  description: "Party list",
};

export default async function Page() {
  return <ConstituencyListPage />;
}
