"use client";

import { Row } from "@/components/row";
import { DivisionItemCard } from "@/features/cards";
import { MemberVoteDescription, MemberVoteIcon } from "@/features/division";
import { SearchList } from "@/features/paginated";
import { Props } from "@/types/react";

export const MemberVotingHistory = (
  props: Props<
    typeof SearchList,
    {
      parliamentdotuk: number;
    },
    "path" | "params" | "itemComponent"
  >,
) => {
  const { parliamentdotuk, ...rest } = props;
  return (
    <SearchList
      path="/api/members/{parliamentdotuk}/votes/"
      params={{ path: { parliamentdotuk } }}
      itemComponent={(it) => (
        <DivisionItemCard
          key={it.division.parliamentdotuk}
          division={it.division}
          showPassedImage={false}
        >
          <Row className="gap-x-1">
            <MemberVoteIcon vote={it.vote} />
            <MemberVoteDescription vote={it.vote} />
          </Row>
        </DivisionItemCard>
      )}
      {...rest}
    />
  );
};
