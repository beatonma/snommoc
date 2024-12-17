import type { Metadata, ResolvingMetadata } from "next";
import { type ElectionResult, getConstituency, Party } from "@/api";
import ErrorMessage from "@/components/error";
import React, { ReactNode } from "react";
import { Date, DateRange } from "@/components/datetime";
import { ConstituencyMap } from "./map";
import { GeoJSON } from "geojson";
import { partyThemeVariableStyle } from "@/components/themed/party";
import { Optional } from "@/components/optional";
import { MemberItem } from "@/components/item-member";
import { HeaderCard } from "@/components/card";
import { int, Percentage } from "@/components/number";
import { PartyLink, PersonLink } from "@/components/linked-data";
import Links from "@/links";
import { TextLink } from "@/components/link";

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
        <section className="overflow-hidden sm:rounded-lg">
          <ConstituencyMap
            className="aspect-square max-h-[50vh] w-full"
            geojson={
              constituency.boundary
                ? (constituency.boundary as unknown as GeoJSON)
                : undefined
            }
          />

          <HeaderCard
            party={constituency.mp?.party}
            className="!w-full !rounded-none"
          >
            <h1>{constituency.name}</h1>

            {constituency.end == null ? (
              <span>
                Constituency updated <Date date={constituency.start} />
              </span>
            ) : (
              <DateRange start={constituency.start} end={constituency.end} />
            )}
            <Optional
              value={constituency.mp}
              block={(it) => (
                <div className="mt-4">
                  <div className="text-sm">Current MP:</div>
                  <MemberItem
                    className="w-fit !max-w-none [&>*]:!p-0 [&]:hover:after:inset-[-0.5rem]"
                    member={it}
                    showConstituency={false}
                  />
                </div>
              )}
            />
          </HeaderCard>
        </section>

        <section>
          <ElectionResults results={constituency.results} />
        </section>
      </main>
    </div>
  );
}

const ElectionResults = ({ results }: { results: ElectionResult[] }) => {
  if (results.length === 0) return null;

  return (
    <>
      <h2>Election results</h2>
      {results.map((it) => (
        <ElectionResult key={it.election.parliamentdotuk} result={it} />
      ))}
    </>
  );
};

const ElectionResult = (props: { result: ElectionResult }) => {
  const { result } = props;

  /** Any candidate with <5% of votes loses their £500 deposit.
   * {@link Links.ElectoralCommission.CandidateDeposit}.
   * */
  const depositForfeitLimit = result.turnout * 0.05;
  let depositLost = false;

  return (
    <div className="mb-8 mt-4">
      <div className="flex flex-wrap items-baseline gap-2">
        <h3>{result.election.name}</h3>
        <Date date={result.election.date} />
      </div>

      <div className="my-2 border-l border-l-primary pl-2 sm:pl-4">
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

        <table>
          <thead>
            <tr>
              <th>Candidate</th>
              <th>Party</th>
              <th>Votes</th>
              <th>%</th>
            </tr>
          </thead>
          <tbody>
            {result.candidates.map((it) => {
              let extra: ReactNode;
              if (!depositLost && it.votes < depositForfeitLimit) {
                extra = (
                  <tr>
                    <td colSpan={100} className="pt-4">
                      <p className="border-t-[2px] border-dashed border-t-red-500 pt-2 text-center text-sm">
                        <TextLink
                          href={Links.ElectoralCommission.CandidateDeposit}
                        >
                          Deposit lost
                        </TextLink>
                      </p>
                    </td>
                  </tr>
                );
                depositLost = true;
              }
              return (
                <React.Fragment key={it.name}>
                  {extra}
                  <tr>
                    <td>
                      <PersonLink person={it.profile} fallback={it.name} />
                    </td>
                    <td>
                      <PartyLink party={it.party} />
                    </td>
                    <td>{int(it.votes)}</td>
                    <td>
                      <Percentage value={(it.votes / result.turnout) * 100} />
                    </td>
                  </tr>
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
