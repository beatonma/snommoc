import type { Metadata, ResolvingMetadata } from "next";
import React, { CSSProperties, ReactNode } from "react";
import { getOr404 } from "@/api/client";
import { type ElectionResult } from "@/api/schema";
import { InlineLink } from "@/components/button";
import { Callout } from "@/components/callout";
import { Date, DateRange } from "@/components/datetime";
import { Percentage, int } from "@/components/number";
import { Optional, onlyIf } from "@/components/optional";
import { ContentLayout } from "@/components/page-layout";
import { HeaderCard, MemberItemCard } from "@/features/cards";
import { PartyLink, PersonLink } from "@/features/linked-data";
import { itemThemeCss } from "@/features/themed/item-theme";
import { Links } from "@/links";
import { ConstituencyMap } from "./map";

const getConstituency = async (parliamentdotuk: number) =>
  getOr404("/api/constituencies/{parliamentdotuk}/", {
    path: { parliamentdotuk },
  });

type PageProps = {
  params: Promise<{ parliamentdotuk: number }>;
};

export async function generateMetadata(
  { params }: PageProps,
  parent: ResolvingMetadata,
): Promise<Metadata> {
  const parliamentdotuk = (await params).parliamentdotuk;
  const constituency = await getConstituency(parliamentdotuk);

  const parentTitle = (await parent).title?.absolute;
  return {
    title: constituency ? `${constituency.name} - ${parentTitle}` : parentTitle,
    description: `Constituency profile`,
  };
}

export default async function ConstituencyDetailPage({ params }: PageProps) {
  const parliamentdotuk = (await params).parliamentdotuk;
  const constituency = await getConstituency(parliamentdotuk);

  return (
    <ContentLayout
      layout="CenteredReadable"
      style={itemThemeCss(constituency.mp?.party)}
    >
      <section>
        <HeaderCard
          themeSource={undefined} /* Inherit from ContentLayout */
          hero={onlyIf(
            constituency.boundary,
            <ConstituencyMap
              constituency={constituency}
              className="aspect-square max-h-[50vh] w-full"
            />,
          )}
        >
          <div className="space-y-2">
            <h1>{constituency.name}</h1>

            <Optional
              value={constituency.end != null}
              block={() => (
                <>
                  <DateRange
                    start={constituency.start}
                    end={constituency.end}
                  />
                  <Callout>
                    This is a historical constituency - available data may be
                    limited.
                  </Callout>
                </>
              )}
            />

            <Optional
              value={constituency.mp}
              block={(it) => (
                <MemberItemCard
                  className="w-full max-w-none [box-shadow:none]"
                  member={it}
                  showConstituency={false}
                  label="Current MP"
                />
              )}
            />
          </div>
        </HeaderCard>
      </section>

      <section>
        <ElectionResults results={constituency.results} />
      </section>
    </ContentLayout>
  );
}

const ElectionResults = ({ results }: { results: ElectionResult[] }) => {
  if (results.length === 0) return null;

  return (
    <>
      <h2 className="px-edge">Election results</h2>
      {results.map((it) => (
        <ElectionResult key={it.election.parliamentdotuk} result={it} />
      ))}
    </>
  );
};

const ElectionResult = (props: { result: ElectionResult }) => {
  const { result } = props;

  return (
    <section>
      <div className="px-edge flex flex-wrap items-baseline gap-2">
        <h3>{result.election.name}</h3>
        <Date date={result.election.date} dateFormat="Short" />
      </div>

      <div className="border-l-primary my-2 border-l pl-2 sm:pl-4">
        <div className="pb-4 text-lg">
          <div className="font-bold">
            <PartyLink party={result.winner?.party} />{" "}
            {result.result.toUpperCase()}
          </div>
          <div>
            Turnout:{" "}
            <Percentage
              value={(result.turnout / result.electorate) * 100}
              title={`${int(result.turnout)} of ${int(result.electorate)}`}
            />
          </div>
        </div>

        <table className="w-full card surface">
          <thead>
            <tr>
              <th className="text-left">Candidate</th>
              <th className="text-left">Party</th>
              <th className="text-right">Votes</th>
              <th className="text-right">%</th>
            </tr>
          </thead>
          <tbody>
            <Candidates
              candidates={result.candidates}
              turnout={result.turnout}
            />
          </tbody>
        </table>
      </div>
    </section>
  );
};

type Candidate = ElectionResult["candidates"][number];
type CandidateOrMessage = Candidate | "DEPOSIT_LOST";

const Candidates = (props: {
  candidates: ElectionResult["candidates"];
  turnout: number;
}) => {
  const { candidates, turnout } = props;

  /** Any candidate with <5% of votes loses their £500 deposit.
   * {@link Links.ElectoralCommission.CandidateDeposit}.
   * */
  const depositForfeitLimit = turnout * 0.05;
  const depositLostIndex = candidates.findIndex(
    (it) => it.votes < depositForfeitLimit,
  );
  const annotatedCandidates: CandidateOrMessage[] = [...candidates];
  if (depositLostIndex >= 0) {
    // depositLostIndex will be -1 if all candidates kept their deposit
    annotatedCandidates.splice(depositLostIndex, 0, "DEPOSIT_LOST");
  }

  return (
    <AnnotatedCandidates candidates={annotatedCandidates} turnout={turnout} />
  );
};

const AnnotatedCandidates = (props: {
  candidates: CandidateOrMessage[];
  turnout: number;
}) => {
  const { candidates, turnout } = props;

  return (
    <>
      {candidates.map((item) => {
        if (item == "DEPOSIT_LOST") {
          return <DepositLostTableRow key={item} />;
        } else {
          return (
            <CandidateTableRow
              key={item.name}
              candidate={item}
              turnout={turnout}
            />
          );
        }
      })}
    </>
  );
};

const CandidateTableRow = (props: {
  candidate: Candidate;
  turnout: number;
}) => {
  const { candidate, turnout } = props;
  return (
    <tr>
      <td>
        <PersonLink person={candidate.profile} fallback={candidate.name} />
      </td>
      <td>
        <PartyLink party={candidate.party} />
      </td>
      <td className="text-right">{int(candidate.votes)}</td>
      <td className="text-right">
        <Percentage value={(candidate.votes / turnout) * 100} />
      </td>
    </tr>
  );
};

const DepositLostTableRow = () => {
  return (
    <tr className="hover:bg-inherit colorful-links">
      <th colSpan={100} className="text-left border-r-0">
        <div className="border-y-[2px] border-dashed border-current/20 py-2 text-sm font-normal">
          <span>Candidates with less than 5% of the vote </span>
          <InlineLink
            style={{ "--primary": "currentColor" } as CSSProperties}
            href={Links.ElectoralCommission.CandidateDeposit}
          >
            forfeit their deposit
          </InlineLink>
          .
        </div>
      </th>
    </tr>
  );
};
