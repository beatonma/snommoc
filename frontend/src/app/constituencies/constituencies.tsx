"use client";

import { type ConstituencyMini } from "@/api";
import React from "react";
import { SearchList } from "@/components/paginated/search-list";
import { ListItemCard } from "@/components/card";
import { DateRange } from "@/components/datetime";
import { OptionalDiv } from "@/components/optional";
import { SeparatedRow } from "@/components/collection";

export default function ConstituencyList() {
  return (
    <SearchList
      path="/api/constituencies/"
      itemComponent={(constituency) => (
        <Constituency key={constituency.parliamentdotuk} {...constituency} />
      )}
    />
  );
}

const Constituency = (props: ConstituencyMini) => {
  const { parliamentdotuk, name, start, end, mp } = props;

  return (
    <ListItemCard
      href={`/constituencies/${parliamentdotuk}/`}
      party={mp?.party}
    >
      <h2>{name}</h2>

      <SeparatedRow>
        <OptionalDiv value={mp?.party?.name} />
        <OptionalDiv value={mp?.name} />
      </SeparatedRow>

      <DateRange start={start} end={end} />
    </ListItemCard>
  );
};
