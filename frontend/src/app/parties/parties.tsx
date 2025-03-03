"use client";

import React from "react";
import { SearchList } from "@/components/paginated/search-list";
import { GridSectionHeader } from "@/components/grid";
import { PartyItemCard } from "@/components/models/list-item";

export default function PartyList() {
  return (
    <SearchList
      path="/api/parties/"
      itemComponent={(party, index, arr) => {
        if (
          index > 0 &&
          party.active_commons_members === null &&
          (arr[index - 1]?.active_commons_members ?? null) !== null
        ) {
          return (
            <React.Fragment key={party.parliamentdotuk}>
              <GridSectionHeader>No current MPs</GridSectionHeader>
              <PartyItemCard party={party} />
            </React.Fragment>
          );
        }

        if (
          index > 0 &&
          party.active_member_count === 0 &&
          (arr[index - 1]?.active_member_count ?? 0) > 0
        ) {
          return (
            <React.Fragment key={party.parliamentdotuk}>
              <GridSectionHeader>No current Members</GridSectionHeader>
              <PartyItemCard party={party} />
            </React.Fragment>
          );
        }

        return <PartyItemCard key={party.parliamentdotuk} party={party} />;
      }}
    />
  );
}

// const Party = (props: { party: Party } & ComponentPropsWithoutRef<"a">) => {
//   const { party, className, ...rest } = props;
//
//   return (
//     <ListItemCard
//       href={`/parties/${party.parliamentdotuk}/`}
//       party={party}
//       image={<OptionalSvg src={party.logo} alt={party.name} className="p-2" />}
//       {...rest}
//     >
//       <h2>{party.name}</h2>
//
//       <span>{partyMemberSummary(party)}</span>
//     </ListItemCard>
//   );
// };
//
// const partyMemberSummary = (party: Party) => {
//   const mps = party.active_commons_members;
//   const lords = party.active_member_count - (party.active_commons_members ?? 0);
//
//   const parts = [];
//   if (mps) parts.push(plural("MP", mps));
//   if (lords) parts.push(plural("Lord", lords));
//
//   return parts.join(", ");
// };
