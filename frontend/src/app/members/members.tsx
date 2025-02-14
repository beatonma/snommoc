"use client";
import { Fixtures, Query } from "@/api";
import React, { ReactNode } from "react";
import { SearchFilters, SearchList } from "@/components/paginated/search-list";
import { MemberItem } from "@/components/item-member";

export default function MembersList(props: {
  header?: ReactNode;
  searchFilters?: SearchFilters;
  immutableFilters?: Query<"/api/members/">;
}) {
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
        <MemberItem key={member.parliamentdotuk} member={member} />
      )}
    />
  );
}
