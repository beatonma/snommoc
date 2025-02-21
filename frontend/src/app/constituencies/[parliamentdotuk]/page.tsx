import type { Metadata, ResolvingMetadata } from "next";
import { type ElectionResult, get } from "@/api";
import ErrorMessage from "@/components/error";
import React, { ReactNode } from "react";
import { Date, DateRange } from "@/components/datetime";
import { ConstituencyMap } from "./map";
import { partyColors } from "@/components/themed/party";
import { Optional } from "@/components/optional";
import { MemberItem } from "@/components/item-member";
import { HeaderCard } from "@/components/card";
import { int, Percentage } from "@/components/number";
import { PartyLink, PersonLink } from "@/components/linked-data";
import Links from "@/links";
import { TextLink } from "@/components/link";
import PageLayout from "@/components/page";
import WindowInsets from "@/components/insets";

const getConstituency = async (parliamentdotuk: number) =>
  get("/api/constituencies/{parliamentdotuk}/", {
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
  const constituency = (await getConstituency(parliamentdotuk)).data;

  const parentTitle = (await parent).title?.absolute;
  return {
    title: constituency ? `${constituency.name} - ${parentTitle}` : parentTitle,
    description: `Constituency profile`,
  };
}

export default async function Page({ params }: PageProps) {
  const parliamentdotuk = (await params).parliamentdotuk;
  const constituency = (await getConstituency(parliamentdotuk)).data;

  if (!constituency) return <ErrorMessage />;

  return (
    <PageLayout
      layout="CenteredReadable"
      style={partyColors(constituency.mp?.party)}
    >
      <section className="gap-y-0 overflow-hidden sm:rounded-lg">
        <ConstituencyMap
          constituency={constituency}
          className="aspect-square max-h-[50vh] w-full"
        />

        <HeaderCard
          party={constituency.mp?.party}
          className="w-full! rounded-none!"
        >
          <h1>{constituency.name}</h1>

          <Optional
            value={constituency.end != null}
            block={() => (
              <DateRange start={constituency.start} end={constituency.end} />
            )}
          />
          <Optional
            value={constituency.mp}
            block={(it) => (
              <div className="mt-4">
                <div className="text-sm">Current MP:</div>
                <MemberItem
                  className="w-fit max-w-none! *:p-0! [&]:hover:after:inset-[-0.5rem]"
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
    </PageLayout>
  );
}

const ElectionResults = ({ results }: { results: ElectionResult[] }) => {
  if (results.length === 0) return null;

  return (
    <>
      <h2 className={WindowInsets}>Election results</h2>
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
    <section>
      <div className={`${WindowInsets} flex flex-wrap items-baseline gap-2`}>
        <h3>{result.election.name}</h3>
        <Date date={result.election.date} />
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

        <table className="w-full">
          <thead>
            <tr>
              <th className="text-left">Candidate</th>
              <th className="text-left">Party</th>
              <th className="text-right">Votes</th>
              <th className="text-right">%</th>
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
                    <td className="text-right">{int(it.votes)}</td>
                    <td className="text-right">
                      <Percentage value={(it.votes / result.turnout) * 100} />
                    </td>
                  </tr>
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
};
