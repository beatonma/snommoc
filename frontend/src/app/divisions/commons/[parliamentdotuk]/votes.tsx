"use client";

import { useMemo } from "react";
import { Fixtures } from "@/api";
import { MemberItemCard } from "@/components/models/list-item";
import { SearchList } from "@/components/paginated/search-list";
import { MemberVoteDescription, MemberVoteIcon } from "./_components";

export default function DivisionVotes({
  parliamentdotuk,
}: {
  parliamentdotuk: number;
}) {
  const paramsMemo = useMemo(
    () => ({ path: { parliamentdotuk } }),
    [parliamentdotuk],
  );

  return (
    <SearchList
      path="/api/divisions/commons/{parliamentdotuk}/votes/"
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
}
