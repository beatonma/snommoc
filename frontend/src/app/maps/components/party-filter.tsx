import { PartyTerritory } from "@/api";
import React, { ComponentPropsWithoutRef } from "react";
import { classes } from "@/util/transforms";

export const PartyTerritoryKey = (
  props: {
    parties: PartyTerritory[] | undefined;
    onClickParty: (partyId: number) => void;
  } & ComponentPropsWithoutRef<"ul">,
) => {
  const { parties, onClickParty, ...rest } = props;
  if (!parties) return null;
  return (
    <ul {...rest}>
      {parties.map((party) => (
        <li
          key={party.parliamentdotuk}
          className={classes(
            "row surface-hover chip-content pointer-events-auto w-fit cursor-pointer list-none gap-1.5",
            "md:bg-surface/80",
            "max-md:chip",
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
