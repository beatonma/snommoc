"use client";

import React, { ReactNode } from "react";
import { Query } from "@/api/client";
import { Fixtures } from "@/api/schema";
import { MemberItemCard } from "@/features/cards";
import { SearchFilters, SearchList } from "@/features/paginated/search-list";

export const MembersList = (props: {
  header?: ReactNode;
  searchFilters?: SearchFilters;
  immutableFilters?: Query<"/api/members/">;
}) => {
  const propFilters = props.searchFilters ?? {};
  const searchFilters = {
    singleChoice: {
      house: {
        label: "House",
        value: undefined,
        values: [
          { display: "All", value: undefined },
          ...Fixtures.HouseTypeValues,
        ],
      },
      status: {
        label: "Status",
        value: "current",
        values: Fixtures.MemberStatusValues,
      },
      ...propFilters.singleChoice,
    },
    bool: { ...propFilters.bool },
  };

  return (
    <SearchList
      header={props.header}
      path="/api/members/"
      searchFilters={searchFilters}
      immutableFilters={props.immutableFilters}
      itemComponent={(member) => (
        <MemberItemCard key={member.parliamentdotuk} member={member} />
      )}
    />
  );
};
