import { CommonsDivision, HouseType, LordsDivision } from "@/api";
import {
  DivisionVotes,
  DivisionVotesProps,
} from "@/app/divisions/_components/votes";
import { TextButton } from "@/components/button";
import { Date, DateFormat } from "@/components/datetime";
import { PageLayout } from "@/components/page-layout";
import { Prose } from "@/components/prose";
import { Row } from "@/components/row";
import { houseSurface } from "@/components/themed/tailwind";
import { classes } from "@/util/transforms";

type Division = CommonsDivision | LordsDivision;

export const DivisionPage = ({
  division,
  votes,
}: {
  division: Division;
  votes: DivisionVotesProps;
}) => {
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

      <PageLayout layout="CenteredFeed">
        <DivisionVotes
          path={votes.path}
          parliamentdotuk={votes.parliamentdotuk}
        />
      </PageLayout>
    </div>
  );
};

const House = ({ house }: { house: HouseType }) => (
  <div className={classes(houseSurface(house), "chip chip-content w-fit")}>
    House of {house}
  </div>
);

const Verdict = ({ division }: { division: Division }) => {
  return (
    <Prose
      className={classes(
        "surface card card-content",
        division.is_passed
          ? "[--primary:var(--color-positive)]"
          : "[--primary:var(--color-negative)]",
      )}
    >
      <blockquote className="text-xl">
        The{" "}
        <strong className="text-current/80">
          {division.is_passed ? "ayes" : "noes"}
        </strong>{" "}
        have it!
      </blockquote>
      <p className="pb-0">
        The motion {division.is_passed ? "passed" : "did not pass"}.
      </p>
      <Row className="flex-wrap gap-x-4 text-sm">
        <TextButton icon="Upvote">{division.ayes} voted in favour</TextButton>
        <TextButton icon="Downvote">{division.noes} voted against</TextButton>
        {"did_not_vote" in division ? (
          <TextButton icon="DidNotVote">
            {division.did_not_vote} did not vote
          </TextButton>
        ) : undefined}
      </Row>
    </Prose>
  );
};
