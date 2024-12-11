"use client";
import {
  Fixtures,
  getMembers,
  type MemberFilters,
  type MemberMiniSchema,
} from "@/api";
import { MemberPortrait } from "@/components/member-portrait";
import { OptionalDiv } from "@/components/optional";
import React, { ReactNode } from "react";
import { SearchFilters, SearchList } from "@/components/paginated/search-list";
import { ListItemCard } from "@/components/card";

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
        <Member key={member.parliamentdotuk} {...member} />
      )}
    />
  );
}

const Member = (props: MemberMiniSchema) => {
  return (
    <ListItemCard
      href={`/members/${props.parliamentdotuk}/`}
      party={props.party}
      title={`${props.parliamentdotuk}`}
      image={
        <MemberPortrait
          name={props.name}
          src={props.portrait}
          className="size-16 shrink-0 overflow-hidden rounded-md bg-primary-900"
        />
      }
    >
      <h2>{props.name}</h2>
      <OptionalDiv
        title="Current post"
        value={props.current_posts}
        className="line-clamp-1"
      />
      <div className="separated flex flex-wrap">
        <OptionalDiv
          title="Party"
          value={props.party?.name}
          className="line-clamp-1"
        />
        <OptionalDiv
          title="Constituency"
          value={props.constituency?.name}
          className="line-clamp-1"
        />
      </div>
    </ListItemCard>
  );
};
