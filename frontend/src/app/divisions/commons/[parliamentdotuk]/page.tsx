import type { Metadata, ResolvingMetadata } from "next";
import { getOr404 } from "@/api";
import { DivisionPage } from "../../_components";

type PageProps = {
  params: Promise<{ parliamentdotuk: number }>;
};

const getDivision = async (parliamentdotuk: number) =>
  getOr404("/api/divisions/commons/{parliamentdotuk}/", {
    path: { parliamentdotuk },
  });

export async function generateMetadata(
  { params }: PageProps,
  parent: ResolvingMetadata,
): Promise<Metadata> {
  const parliamentdotuk = (await params).parliamentdotuk;
  const division = await getDivision(parliamentdotuk);
  const parentTitle = (await parent).title?.absolute;
  return {
    title: division ? `${division.title} - ${parentTitle}` : parentTitle,
    description: `House division`,
  };
}

export default async function CommonsDivisionPage({ params }: PageProps) {
  const parliamentdotuk = (await params).parliamentdotuk;
  const division = await getDivision(parliamentdotuk);

  return (
    <DivisionPage
      division={division}
      votes={{
        path: "/api/divisions/commons/{parliamentdotuk}/votes/",
        parliamentdotuk,
      }}
    />
  );
}
