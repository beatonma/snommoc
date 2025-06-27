"use client";

import React from "react";
import { GridSectionHeader } from "@/components/grid";
import { PartyItemCard } from "@/features/cards";
import { SearchList } from "@/features/paginated/search-list";

export const PartyList = () => (
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
