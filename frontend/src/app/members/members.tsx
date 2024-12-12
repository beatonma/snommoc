"use client";
import { Fixtures, getMembers, type MemberFilters } from "@/api";
import React, { ReactNode } from "react";
import { SearchFilters, SearchList } from "@/components/paginated/search-list";
import { MemberItem } from "@/components/item-member";

export default function MembersList(props: {
  header?: ReactNode;
  searchFilters?: SearchFilters;
  immutableFilters?: MemberFilters;
}) {
  const propSearchFilters: SearchFilters = props.searchFilters ?? {};
  const searchFilters: SearchFilters = {
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
      ...propSearchFilters.singleChoice,
    },
    bool: { ...propSearchFilters.bool },
  };

  return (
    <SearchList
      header={props.header}
      loader={getMembers}
      searchFilters={searchFilters}
      immutableFilters={props.immutableFilters}
      itemComponent={(member) => (
        <MemberItem key={member.parliamentdotuk} member={member} />
      )}
    />
  );
}
