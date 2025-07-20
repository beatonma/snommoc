"use client";

import { CSSProperties } from "react";
import { BillItemCard } from "@/features/cards/list-item";
import { SearchList } from "@/features/paginated";

export const BillsList = () => {
  return (
    <SearchList
      path="/api/bills/"
      itemComponent={(it) => (
        <BillItemCard key={it.parliamentdotuk} bill={it} />
      )}
      style={
        {
          "--spacing-listitem-card": "var(--spacing-listitem-card-wide)",
        } as CSSProperties
      }
    />
  );
};
