"use client";

import { getConstituencies, type ConstituencyMini } from "@/api";
import Link from "next/link";
import React from "react";
import { SearchListPage } from "@/components/page/list-page";

export default function ConstituencyList() {
  return (
    <SearchListPage
      loader={getConstituencies}
      itemComponent={(constituency) => (
        <Constituency key={constituency.parliamentdotuk} {...constituency} />
      )}
    />
  );
}

const Constituency = (props: ConstituencyMini) => {
  const { parliamentdotuk, name } = props;

  return (
    <Link
      href={`/constituencies/${props.parliamentdotuk}/`}
      className="flex overflow-hidden sm:rounded-lg"
    >
      <div className="flex grow gap-3 p-3">
        <div className="flex flex-col gap-0.5 [&>div]:text-sm">
          <h2 className="text-xl font-semibold">{name}</h2>
        </div>
      </div>
    </Link>
  );
};
