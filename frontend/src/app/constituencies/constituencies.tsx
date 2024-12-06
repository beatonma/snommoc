"use client";

import { getConstituencies, type ConstituencyMini } from "@/api";
import React from "react";
import { SearchList } from "@/components/paginated/search-list";
import { ListItemCard } from "@/components/card";

export default function ConstituencyList() {
  return (
    <SearchList
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
    <ListItemCard href={`/constituencies/${parliamentdotuk}/`}>
      <h2>{name}</h2>
    </ListItemCard>
  );
};
