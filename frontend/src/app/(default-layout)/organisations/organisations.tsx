"use client";

import { SearchList } from "@/features/paginated";
import { OrganisationItemCard } from "@/features/cards/list-item";

export const OrganisationsList = () => {
  return <SearchList path="/api/organisations/" itemComponent={it => <OrganisationItemCard organisation={it} />} />
}
