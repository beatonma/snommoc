import { Metadata } from "next";
import { PageLayout } from "@/components/page-layout";
import { DivisionsList } from "./divisions";

export const metadata: Metadata = {
  title: "Divisions",
  description: "Parliamentary divisions",
};

export default async function DivisionsListPage() {
  return (
    <PageLayout layout="CenteredFeed">
      <DivisionsList />
    </PageLayout>
  );
}
