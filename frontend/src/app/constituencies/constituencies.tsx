"use client";

import React from "react";
import { ConstituencyItemCard } from "@/components/models/list-item";
import { SearchList } from "@/components/paginated/search-list";

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
