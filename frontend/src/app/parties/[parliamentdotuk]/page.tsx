import type { Metadata, ResolvingMetadata } from "next";
import { getParty } from "@/api";
import ErrorMessage from "@/components/error";
import React from "react";
import { DetailPage } from "@/components/page/detail-page";

type PageProps = {
  params: Promise<{ parliamentdotuk: number }>;
};

export async function generateMetadata(
  { params }: PageProps,
  parent: ResolvingMetadata,
): Promise<Metadata> {
  const parliamentdotuk = (await params).parliamentdotuk;
  const party = (await getParty(parliamentdotuk)).data;
  const parentTitle = (await parent).title?.absolute;
  return {
    title: party ? `${party.name} - ${parentTitle}` : parentTitle,
    description: `Party profile`,
  };
}

export default async function Page({ params }: PageProps) {
  const parliamentdotuk = (await params).parliamentdotuk;
  const response = await getParty(parliamentdotuk);
  const party = response.data;

  if (!party) return <ErrorMessage />;

  return (
    <DetailPage>
      <div>{party.logo}</div>
      <div>{party.name}</div>
      <div>{party.long_name}</div>
      <div>{party.year_founded}</div>

      <div>{party.homepage}</div>
      <div>{party.wikipedia}</div>
    </DetailPage>
  );
}
