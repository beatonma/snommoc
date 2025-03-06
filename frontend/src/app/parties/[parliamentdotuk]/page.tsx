import type { Metadata, ResolvingMetadata } from "next";
import React from "react";
import { GenderDemographics, LordsDemographics, PartyDetail, get } from "@/api";
import MembersList from "@/app/members/members";
import { HeaderCard } from "@/components/card";
import ErrorMessage from "@/components/error";
import { OptionalSvg } from "@/components/image";
import { LinkGroup } from "@/components/link";
import { OptionalDiv } from "@/components/optional";
import PageLayout from "@/components/page-layout";
import { partyColors } from "@/components/themed/party";
import { plural } from "@/util/plurals";

type PageProps = {
  params: Promise<{ parliamentdotuk: number }>;
};

const getParty = async (parliamentdotuk: number) =>
  get("/api/parties/{parliamentdotuk}/", {
    path: { parliamentdotuk },
  });

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
  const party = (await getParty(parliamentdotuk)).data;

  if (!party) return <ErrorMessage />;

  return (
    <>
      <PageLayout layout="CenteredReadable" style={partyColors(party)}>
        <section>
          <HeaderCard
            party={party}
            image={
              <OptionalSvg
                src={party.logo}
                alt={party.name}
                className="w-32 shrink-0 overflow-hidden rounded-md bg-white/75 p-2"
                priority
              />
            }
          >
            <h1>{party.name}</h1>

            <OptionalDiv
              value={party.short_name}
              condition={(it) => it !== party.name}
            />
            <OptionalDiv
              value={party.long_name}
              condition={(it) => it !== party.name}
            />
            <OptionalDiv
              value={party.year_founded}
              condition={Boolean}
              block={(founded) => `Founded ${founded}`}
            />
            <OptionalDiv
              value={party.active_member_count}
              block={(count) =>
                `${plural("Member", count).toLowerCase()} in Parliament`
              }
            />

            <LinkGroup links={[party.homepage, party.wikipedia]} />
          </HeaderCard>
        </section>

        <section className="insets-x">
          <Demographics party={party} />
        </section>
      </PageLayout>

      <PageLayout layout="CenteredFeed" mainElement="aside">
        <MembersList
          header={<h2>Members</h2>}
          immutableFilters={{ party: party.parliamentdotuk }}
        />
      </PageLayout>
    </>
  );
}

const Demographics = (props: { party: PartyDetail }) => {
  const { party } = props;

  if (!party.gender_demographics && !party.lords_demographics) return null;

  return (
    <>
      <h2>Demographics</h2>
      <div className="flex flex-row flex-wrap gap-4">
        <_GenderDemographics demographics={party.gender_demographics} />
        <_LordsDemographics demographics={party.lords_demographics} />
      </div>
    </>
  );
};

const _GenderDemographics = (props: { demographics: GenderDemographics[] }) => {
  const { demographics } = props;
  return (
    <table>
      <thead>
        <tr>
          <th />
          {demographics.map((it) => (
            <th key={it.house} className="text-right">
              {it.house}
            </th>
          ))}
        </tr>
      </thead>

      <tbody className="[&_td]:text-right">
        <tr>
          <th>Male</th>
          {demographics.map((it) => (
            <td key={it.house}>{it.male_member_count}</td>
          ))}
        </tr>
        <tr>
          <th>Female</th>
          {demographics.map((it) => (
            <td key={it.house}>{it.female_member_count}</td>
          ))}
        </tr>
        <tr>
          <th>Non-Binary</th>
          {demographics.map((it) => (
            <td key={it.house}>{it.non_binary_member_count}</td>
          ))}
        </tr>
        <tr>
          <th>Total</th>
          {demographics.map((it) => (
            <td key={it.house}>{it.total_member_count}</td>
          ))}
        </tr>
      </tbody>
    </table>
  );
};

const _LordsDemographics = (props: {
  demographics: LordsDemographics | null | undefined;
}) => {
  const { demographics } = props;
  if (!demographics) return null;

  return (
    <table>
      <thead>
        <tr>
          <th colSpan={2} className="text-center">
            Lords type
          </th>
        </tr>
      </thead>

      <tbody className="[&_td]:text-right">
        <tr>
          <th>Bishops</th>
          <td>{demographics.bishop_count}</td>
        </tr>
        <tr>
          <th>Hereditary</th>
          <td>{demographics.hereditary_count}</td>
        </tr>
        <tr>
          <th>Life</th>
          <td>{demographics.life_count}</td>
        </tr>
        <tr>
          <th>Total</th>
          <td>{demographics.total_count}</td>
        </tr>
      </tbody>
    </table>
  );
};
