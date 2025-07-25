"use client";

import { DivisionItemCard } from "@/features/cards";
import { SearchList } from "@/features/paginated/search-list";

export const DivisionsList = () => (
  <SearchList
    path="/api/divisions/"
    itemComponent={(division) => (
      <DivisionItemCard key={division.parliamentdotuk} division={division} />
    )}
    className="wide-cards"
  />
);
