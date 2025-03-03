"use client";

import React from "react";
import { SearchList } from "@/components/paginated/search-list";
import { ConstituencyItemCard } from "@/components/models/list-item";

export default function ConstituencyList() {
  return (
    <SearchList
      path="/api/constituencies/"
      itemComponent={(constituency) => (
        <ConstituencyItemCard
          key={constituency.parliamentdotuk}
          constituency={constituency}
        />
      )}
    />
  );
}
