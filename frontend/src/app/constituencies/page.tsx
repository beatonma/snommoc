import React from "react";
import { Metadata } from "next";
import ConstituencyListPage from "@/app/constituencies/constituencies";

export const metadata: Metadata = {
  title: "Constituencies",
  description: "Constituency list",
};

export default async function Page() {
  return (
    <main>
      <ConstituencyListPage />
    </main>
  );
}
