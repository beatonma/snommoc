import { Metadata } from "next";
import { DivisionsList } from "@/app/divisions/divisions";
import { PageLayout } from "@/components/page-layout";

export const metadata: Metadata = {
  title: "Divisions",
  description: "Parliamentary divisions",
};

export default async function Page() {
  return (
    <PageLayout layout="CenteredFeed">
      <DivisionsList />
    </PageLayout>
  );
}
