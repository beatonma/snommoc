import type { Metadata, ResolvingMetadata } from "next";
import { getConstituency, MemberMiniSchema } from "@/api";
import ErrorMessage from "@/components/error";
import React from "react";
import { Date, DateRange } from "@/components/datetime";
import { ConstituencyMap } from "./map";
import { GeoJSON } from "geojson";
import { partyThemeVariableStyle } from "@/components/themed/party";
import { MemberPortrait } from "@/components/member-portrait";
import { OptionalDiv } from "@/components/optional";
import { ListItemCard } from "@/components/card";

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
          <Member mp={constituency.mp} />

          <pre>{JSON.stringify(constituency.results, null, 1)}</pre>
        </section>
      </main>
    </div>
  );
}

const Member = (props: { mp: MemberMiniSchema | null }) => {
  const { mp } = props;
  if (!mp) return null;
  return (
    <ListItemCard
      href={`/members/${mp.parliamentdotuk}/`}
      party={mp.party}
      title={`${mp.parliamentdotuk}`}
      image={
        <MemberPortrait
          name={mp.name}
          src={mp.portrait}
          className="size-16 shrink-0 overflow-hidden rounded-md bg-primary-900"
        />
      }
    >
      <h2>{mp.name}</h2>
      <OptionalDiv
        title="Current post"
        value={mp.current_posts}
        className="line-clamp-1"
      />
      <OptionalDiv
        title="Party"
        value={mp.party?.name}
        className="line-clamp-1"
      />
    </ListItemCard>
  );
};
