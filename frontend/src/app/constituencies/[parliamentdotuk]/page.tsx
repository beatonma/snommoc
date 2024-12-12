import type { Metadata, ResolvingMetadata } from "next";
import { getConstituency, MemberMiniSchema } from "@/api";
import ErrorMessage from "@/components/error";
import React from "react";
import { Date, DateRange } from "@/components/datetime";
import { ConstituencyMap } from "./map";
import { GeoJSON } from "geojson";
import { partyThemeVariableStyle } from "@/components/themed/party";
import { Optional } from "@/components/optional";
import { MemberItem } from "@/components/item-member";

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
    <div
      style={partyThemeVariableStyle(constituency.mp?.party)}
      className="flex flex-col items-center gap-y-16"
    >
      <main className="readable w-full">
        <section>
          <ConstituencyMap
            className="aspect-[4/3] w-full overflow-hidden rounded-lg"
            geojson={
              constituency.boundary
                ? (constituency.boundary as unknown as GeoJSON)
                : undefined
            }
          />
        </section>

        <section>
          <h1>{constituency.name}</h1>
          {constituency.end == null ? (
            <span>
              Since <Date date={constituency.start} />
            </span>
          ) : (
            <DateRange start={constituency.start} end={constituency.end} />
          )}
        </section>

        <section>
          <Optional
            value={constituency.mp}
            block={(it) => (
              <MemberItem
                label="Current MP"
                member={it}
                className="max-w-[400px]"
                showConstituency={false}
              />
            )}
          />

          <pre>{JSON.stringify(constituency.results, null, 1)}</pre>
        </section>
      </main>
    </div>
  );
}
