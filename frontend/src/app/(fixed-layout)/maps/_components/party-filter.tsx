import React from "react";
import { PartyTerritory } from "@/api/schema";
import { PartyLink } from "@/features/linked-data";
import { Props } from "@/types/react";
import { addClass } from "@/util/transforms";

export const PartyTerritoryKey = (
  props: Props<
    "ul",
    {
      focussedPartyId: number | undefined;
      parties: PartyTerritory[] | undefined;
      onClickParty: (partyId: number) => void;
    }
  >,
) => {
  const { parties, focussedPartyId, onClickParty, ...rest } = addClass(
    props,
    "list-none",
  );
  if (!parties) return null;
  return (
    <ul {...rest}>
      {parties.map((party) => (
        <li key={party.parliamentdotuk}>
          <PartyLink
            party={party}
            onClick={() => onClickParty(party.parliamentdotuk)}
          />
        </li>
      ))}
    </ul>
  );
};
