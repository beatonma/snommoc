import type { Metadata, ResolvingMetadata } from "next";
import { getOr404 } from "@/api";
import { Placeholder } from "@/components/dev";
import { ContentLayout } from "@/components/page-layout";
import { WebLinks } from "@/features/weblinks";

type PageProps = {
  params: Promise<{ slug: string }>;
};

const getOrganisation = async (slug: string) =>
  getOr404("/api/organisations/{slug}/", {
    path: { slug },
  });

export async function generateMetadata(
  { params }: PageProps,
  parent: ResolvingMetadata,
): Promise<Metadata> {
  const slug = (await params).slug;
  const organisation = await getOrganisation(slug);
  const parentTitle = (await parent).title?.absolute;
  return {
    title: organisation ? `${organisation.name} - ${parentTitle}` : parentTitle,
    description: [`Organisation details`, organisation.name]
      .filter(Boolean)
      .join(": "),
  };
}

export default async function BillDetailPage({ params }: PageProps) {
  const slug = (await params).slug;
  const organisation = await getOrganisation(slug);

  return (
    <ContentLayout layout="CenteredReadable">
      <Placeholder />

      <h2>{organisation.name}</h2>
      <WebLinks links={[organisation.url]} />
    </ContentLayout>
  );
}
