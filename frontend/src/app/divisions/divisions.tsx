"use client";

import { CSSProperties } from "react";
import { DivisionItemCard } from "@/features/cards";
import { SearchList } from "@/features/paginated/search-list";

export const DivisionsList = () => (
  <SearchList
    path="/api/divisions/"
    itemComponent={(division) => (
      <DivisionItemCard key={division.parliamentdotuk} division={division} />
    )}
    style={
      {
        "--spacing-listitem_card": "var(--_spacing-listitem_card_wide)",
      } as CSSProperties
    }
  />
);
