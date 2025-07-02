import { Metadata } from "next";
import { ContentLayout } from "@/components/page-layout";
import { DivisionsList } from "./divisions";

export const metadata: Metadata = {
  title: "Divisions",
  description: "Parliamentary divisions",
};

export default async function DivisionsListPage() {
  return (
    <ContentLayout layout="CenteredFeed">
      <DivisionsList />
    </ContentLayout>
  );
}
