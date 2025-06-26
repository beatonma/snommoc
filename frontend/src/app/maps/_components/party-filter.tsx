import React from "react";
import { PartyTerritory } from "@/api";
import { onlyIf } from "@/components/optional";
import { Props } from "@/types/react";
import { classes } from "@/util/transforms";

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
  const { parties, focussedPartyId, onClickParty, ...rest } = props;
  if (!parties) return null;
  return (
    <ul {...rest}>
      {parties.map((party) => (
        <li
          key={party.parliamentdotuk}
          className={classes(
            "row surface-hover chip chip-content pointer-events-auto w-fit cursor-pointer list-none gap-1.5 border-current/50",
            onlyIf(party.parliamentdotuk === focussedPartyId, "border-2"),
          )}
          onClick={() => onClickParty(party.parliamentdotuk)}
        >
          <div
            className="size-em rounded-sm border-1"
            style={{ backgroundColor: party.theme?.primary }}
          />
          <div className="line-clamp-1">{party.name}</div>
        </li>
      ))}
    </ul>
  );
};
