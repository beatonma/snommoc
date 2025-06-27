"use client";

import { useMemo } from "react";
import { DivisionVoteType, Fixtures } from "@/api/schema";
import Icon, { AppIcon } from "@/components/icon";
import { MemberItemCard } from "@/features/cards";
import { SearchList } from "@/features/paginated/search-list";
import { classes } from "@/util/transforms";

type DivisionVotesPath =
  | "/api/divisions/commons/{parliamentdotuk}/votes/"
  | "/api/divisions/lords/{parliamentdotuk}/votes/";

export interface DivisionVotesProps {
  path: DivisionVotesPath;
  parliamentdotuk: number;
}
export const DivisionVotes = ({
  path,
  parliamentdotuk,
}: DivisionVotesProps) => {
  const paramsMemo = useMemo(
    () => ({ path: { parliamentdotuk } }),
    [parliamentdotuk],
  );

  return (
    <SearchList
      path={path}
      params={paramsMemo}
      searchFilters={{
        singleChoice: {
          vote_type: {
            label: "Vote type",
            value: undefined,
            values: [
              { display: "All", value: undefined },
              ...Fixtures.VoteTypes,
            ],
          },
        },
      }}
      itemComponent={(vote) => (
        <MemberItemCard
          key={vote.person.parliamentdotuk}
          member={vote.person}
          badge={<MemberVoteIcon vote={vote.vote} />}
        >
          <MemberVoteDescription vote={vote.vote} />
        </MemberItemCard>
      )}
    />
  );
};

const MemberVoteIcon = (props: { vote: DivisionVoteType }) => {
  const icons: Record<DivisionVoteType, AppIcon> = {
    aye: "Upvote",
    no: "Downvote",
    did_not_vote: "DidNotVote",
  };
  const icon = icons[props.vote as DivisionVoteType];

  const theme: Record<DivisionVoteType, string> = {
    aye: "surface-positive",
    no: "surface-negative",
    did_not_vote: "surface-scrim",
  };

  return (
    <Icon
      icon={icon}
      className={classes(
        theme[props.vote],
        "size-6 p-1 border-[1px] border-current/60 rounded-md",
      )}
    />
  );
};

const MemberVoteDescription = (props: { vote: DivisionVoteType }) => {
  const descriptions: Record<DivisionVoteType, string> = {
    aye: "Voted in favour",
    no: "Voted against",
    did_not_vote: "Did not vote",
  };
  return descriptions[props.vote] ?? descriptions["did_not_vote"];
};
