import type { Metadata, ResolvingMetadata } from "next";
import { getConstituency } from "@/api";
import ErrorMessage from "@/components/error";
import React from "react";

type PageProps = {
  params: Promise<{ parliamentdotuk: number }>;
};

export async function generateMetadata(
  { params }: PageProps,
  parent: ResolvingMetadata,
): Promise<Metadata> {
  const parliamentdotuk = (await params).parliamentdotuk;
  const constituency = (await getConstituency(parliamentdotuk)).data;
  const parentTitle = (await parent).title?.absolute;
  return {
    title: constituency ? `${constituency.name} - ${parentTitle}` : parentTitle,
    description: `Constituency profile`,
  };
}

export default async function Page({ params }: PageProps) {
  const parliamentdotuk = (await params).parliamentdotuk;
  const response = await getConstituency(parliamentdotuk);
  const constituency = response.data;

  if (!constituency) return <ErrorMessage />;

  return (
    <main>
      <div>{constituency.name}</div>
      <div>{constituency.mp?.name}</div>
      <div>
        {constituency.start} - {constituency.end}
      </div>
      <pre>{JSON.stringify(constituency.boundary)}</pre>
      <pre>{JSON.stringify(constituency.results, null, 1)}</pre>
    </main>
  );
}
