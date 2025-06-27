"use client";

import React from "react";
import { ConstituencyItemCard } from "@/features/cards";
import { SearchList } from "@/features/paginated/search-list";

export const ConstituencyList = () => (
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
