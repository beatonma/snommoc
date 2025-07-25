"use client";

import { BillItemCard } from "@/features/cards/list-item";
import { SearchList } from "@/features/paginated";

export const BillsList = () => {
  return (
    <SearchList
      path="/api/bills/"
      itemComponent={(it) => (
        <BillItemCard key={it.parliamentdotuk} bill={it} />
      )}
      className="wide-cards"
    />
  );
};
