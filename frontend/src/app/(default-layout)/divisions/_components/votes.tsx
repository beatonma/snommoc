"use client";

import { useMemo } from "react";
import { Fixtures } from "@/api/schema";
import { MemberItemCard } from "@/features/cards";
import { MemberVoteDescription, MemberVoteIcon } from "@/features/division";
import { SearchList } from "@/features/paginated/search-list";

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
          badge={
            <MemberVoteIcon
              vote={vote.vote}
              className="size-6 p-1 border-[1px] border-current/60 rounded-md"
            />
          }
        >
          <MemberVoteDescription vote={vote.vote} />
        </MemberItemCard>
      )}
    />
  );
};
