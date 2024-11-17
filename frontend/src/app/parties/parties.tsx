"use client";
import { getParties, type Party } from "@/api";
import Link from "next/link";
import { PartyIconBackground } from "@/components/themed/party";
import React from "react";
import Image from "next/image";
import { SearchListPage } from "@/components/page/list-page";

export default function PartyList() {
  return (
    <SearchListPage
      loader={getParties}
      itemComponent={(party) => (
        <Party key={party.parliamentdotuk} {...party} />
      )}
    />
  );
}

const Party = (props: Party) => {
  const { name, logo } = props;

  return (
    <Link
      href={`/parties/${props.parliamentdotuk}/`}
      className="flex overflow-hidden sm:rounded-lg"
    >
      <PartyIconBackground party={props} className="flex grow gap-3 p-3">
        {logo ? (
          <Image
            src={logo}
            alt={name}
            className="w-16 shrink-0 overflow-hidden rounded-md bg-primary-50 p-2"
            width={64}
            height={64}
          />
        ) : null}

        <div className="flex flex-col gap-0.5 [&>div]:text-sm">
          <h2 className="text-xl font-semibold">{props.name}</h2>
        </div>
      </PartyIconBackground>
    </Link>
  );
};
