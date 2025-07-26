"use client";

import React from "react";
import { GridSectionHeader } from "@/components/grid";
import { PartyItemCard } from "@/features/cards";
import { SearchList } from "@/features/paginated/search-list";
import { plural } from "@/util/plurals";

export const PartyList = () => (
  <SearchList
    path="/api/parties/"
    itemComponent={(party, index, arr) => {
      const previous = arr[index - 1];

      if (party.active_mp_count === 0 && previous?.active_mp_count) {
        return (
          <React.Fragment key={party.parliamentdotuk}>
            <GridSectionHeader>
              No current {plural("MP", 0, (it) => it)}
            </GridSectionHeader>
            <PartyItemCard party={party} />
          </React.Fragment>
        );
      }

      if (
        party.active_mp_count === 0 &&
        party.active_lord_count === 0 &&
        (previous?.active_mp_count || previous?.active_lord_count)
      ) {
        return (
          <React.Fragment key={party.parliamentdotuk}>
            <GridSectionHeader>
              No current {plural("Member", 0, (it) => it)}
            </GridSectionHeader>
            <PartyItemCard party={party} />
          </React.Fragment>
        );
      }

      return <PartyItemCard key={party.parliamentdotuk} party={party} />;
    }}
  />
);
