"use client";
import { getParties, type Party } from "@/api";
import React, { ComponentPropsWithoutRef } from "react";
import { SearchList } from "@/components/paginated/search-list";
import { GridSectionHeader } from "@/components/paginated/pagination";
import { OptionalSvg } from "@/components/image";
import { ListItemCard } from "@/components/card";
import { plural } from "@/util/plurals";

export default function PartyList() {
  return (
    <main>
      <SearchList
        loader={getParties}
        itemComponent={(party, index, arr) => {
          if (
            index > 0 &&
            party.active_commons_members === null &&
            (arr[index - 1]?.active_commons_members ?? null) !== null
          ) {
            return (
              <React.Fragment key={party.parliamentdotuk}>
                <GridSectionHeader>No current MPs</GridSectionHeader>
                <Party party={party} />
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
                <Party party={party} />
              </React.Fragment>
            );
          }

          return <Party key={party.parliamentdotuk} party={party} />;
        }}
      />
    </main>
  );
}

const Party = (props: { party: Party } & ComponentPropsWithoutRef<"a">) => {
  const { party, className, ...rest } = props;

  return (
    <ListItemCard
      href={`/parties/${party.parliamentdotuk}/`}
      party={party}
      image={
        <OptionalSvg
          src={party.logo}
          alt={party.name}
          className="w-16 shrink-0 overflow-hidden rounded-md bg-primary-50 p-2"
        />
      }
      {...rest}
    >
      <h2>{party.name}</h2>

      <span>{partyMemberSummary(party)}</span>
    </ListItemCard>
  );
};

const partyMemberSummary = (party: Party) => {
  const mps = party.active_commons_members;
  const lords = party.active_member_count - (party.active_commons_members ?? 0);

  const parts = [];
  if (mps) parts.push(plural("MP", mps));
  if (lords) parts.push(plural("Lord", lords));

  return parts.join(", ");
};
