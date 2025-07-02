import { CommonsDivision, HouseType, LordsDivision } from "@/api/schema";
import {
  DivisionVotes,
  DivisionVotesProps,
} from "@/app/divisions/_components/votes";
import { InlineButton } from "@/components/button";
import { Date, DateFormat } from "@/components/datetime";
import { ContentLayout } from "@/components/page-layout";
import { Prose } from "@/components/prose";
import { Row } from "@/components/row";
import { houseSurface } from "@/features/themed/tailwind";
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
    <main className="space-y-16">
      <ContentLayout
        layout="CenteredReadable"
        mainElement="div"
        mainClassName="space-y-4"
      >
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
      </ContentLayout>

      <ContentLayout layout="CenteredFeed" mainElement="div">
        <DivisionVotes
          path={votes.path}
          parliamentdotuk={votes.parliamentdotuk}
        />
      </ContentLayout>
    </main>
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
        <InlineButton icon="Upvote">
          {division.ayes} voted in favour
        </InlineButton>
        <InlineButton icon="Downvote">
          {division.noes} voted against
        </InlineButton>
        {"did_not_vote" in division ? (
          <InlineButton icon="DidNotVote">
            {division.did_not_vote} did not vote
          </InlineButton>
        ) : undefined}
      </Row>
    </Prose>
  );
};
