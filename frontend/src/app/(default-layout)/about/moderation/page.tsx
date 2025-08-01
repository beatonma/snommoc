import { Metadata } from "next";
import { ContentLayout } from "@/components/page-layout";
import { Prose } from "@/components/prose";

export const metadata: Metadata = {
  title: "Content moderation",
  description: "Information about content moderation on the Commons service.",
};

export default async function AboutModerationPage() {
  return (
    <ContentLayout layout="CenteredReadable" className="px-edge">
      <Prose>
        <h1>Moderation</h1>

        <p>
          Commons is currently in demo mode: user accounts are not enabled, so
          there is nothing to moderate. This page is kept as a placeholder.
        </p>
      </Prose>
    </ContentLayout>
  );
}
