"use client";

import { CSSProperties } from "react";
import DivisionItemCard from "@/components/models/list-item/division-card";
import { SearchList } from "@/components/paginated/search-list";

export default function DivisionsList() {
  return (
    <SearchList
      path="/api/divisions/recent/"
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
}
