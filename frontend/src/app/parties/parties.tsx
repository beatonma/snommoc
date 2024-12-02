"use client";
import { getParties, type Party } from "@/api";
import Link from "next/link";
import { PartyIconBackground } from "@/components/themed/party";
import React, { ComponentPropsWithoutRef } from "react";
import Image from "next/image";
import { SearchListPage } from "@/components/page/list-page";
import { classes } from "@/util/react";
import { GridSectionHeader } from "@/components/pagination";

export default function PartyList() {
  return (
    <SearchListPage
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
  );
}

const Party = (props: { party: Party } & ComponentPropsWithoutRef<"a">) => {
  const { party, className, ...rest } = props;

  return (
    <Link
      href={`/parties/${party.parliamentdotuk}/`}
      className={classes(className, "flex overflow-hidden sm:rounded-lg")}
      data-active_members={party.active_member_count}
      data-commons={party.active_commons_members}
      {...rest}
    >
      <PartyIconBackground party={party} className="flex grow gap-3 p-3">
        {party.logo ? (
          <Image
            src={party.logo}
            alt={party.name}
            className="w-16 shrink-0 overflow-hidden rounded-md bg-primary-50 p-2"
            width={64}
            height={64}
          />
        ) : null}

        <div className="flex flex-col gap-0.5 [&>div]:text-sm">
          <h2 className="text-xl font-semibold">{party.name}</h2>
        </div>
      </PartyIconBackground>
    </Link>
  );
};
