import type { Metadata, ResolvingMetadata } from "next";
import { CommonsDivision, HouseType, get } from "@/api";
import DivisionVotes from "@/app/divisions/commons/[parliamentdotuk]/votes";
import { TextButton } from "@/components/button";
import { Date, DateFormat } from "@/components/datetime";
import ErrorMessage from "@/components/error";
import PageLayout from "@/components/page-layout";
import Row from "@/components/row";
import { houseSurface } from "@/components/themed/tailwind";
import { classes } from "@/util/transforms";

type PageProps = {
  params: Promise<{ parliamentdotuk: number }>;
};

const getDivision = async (parliamentdotuk: number) =>
  get("/api/divisions/commons/{parliamentdotuk}/", {
    path: { parliamentdotuk },
  });

export async function generateMetadata(
  { params }: PageProps,
  parent: ResolvingMetadata,
): Promise<Metadata> {
  const parliamentdotuk = (await params).parliamentdotuk;
  const division = (await getDivision(parliamentdotuk)).data;
  const parentTitle = (await parent).title?.absolute;
  return {
    title: division ? `${division.title} - ${parentTitle}` : parentTitle,
    description: `House division`,
  };
}

export default async function Page({ params }: PageProps) {
  const parliamentdotuk = (await params).parliamentdotuk;
  const response = await getDivision(parliamentdotuk);
  const division = response.data;

  if (!division) return <ErrorMessage />;

  return (
    <div className="space-y-16">
      <PageLayout layout="CenteredReadable" mainClassName="space-y-4">
        <div className="space-y-1">
          <Row className="gap-x-2">
            <House house={division.house} />

            <Date
              className="text-sm"
              date={division.date}
              dateFormat={DateFormat.FullDate}
            />
          </Row>
          <h1>{division.title}</h1>
        </div>

        <Verdict division={division} />
      </PageLayout>

      <PageLayout layout={"CenteredFeed"}>
        <DivisionVotes parliamentdotuk={parliamentdotuk} />
      </PageLayout>
    </div>
  );
}

const House = ({ house }: { house: HouseType }) => {
  return (
    <div className={classes(houseSurface(house), "chip chip-content w-fit")}>
      House of {house}
    </div>
  );
};

const Verdict = ({ division }: { division: CommonsDivision }) => {
  return (
    <div className={classes("surface card card-content")}>
      <div
        className={classes(
          division.is_passed ? "border-l-positive" : "border-l-negative",
          "[--border-inset:--spacing(1)]",
          "[border-left-width:var(--border-inset)] space-y-1 ps-[calc(var(--border-inset)*2)]",
        )}
      >
        <p className="text-xl">
          The{" "}
          <strong className="text-current/80">
            {division.is_passed ? "ayes" : "noes"}
          </strong>{" "}
          have it!
        </p>
        <p className="text-sm">
          The motion {division.is_passed ? "passed" : "did not pass"}
        </p>
        <Row className="flex-wrap gap-x-4 text-sm">
          <TextButton icon="Upvote">{division.ayes} voted in favour</TextButton>
          <TextButton icon="Downvote">{division.noes} voted against</TextButton>
          <TextButton icon="DidNotVote">
            {division.did_not_vote} did not vote
          </TextButton>
        </Row>
      </div>
    </div>
  );
};
