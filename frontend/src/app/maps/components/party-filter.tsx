import { PartyTerritory } from "@/api";
import React, { ComponentPropsWithoutRef } from "react";
import { addClass, classes } from "@/util/transforms";

export const PartyTerritoryKey = (
  props: {
    parties: PartyTerritory[] | undefined;
    onClickParty: (partyId: number) => void;
  } & ComponentPropsWithoutRef<"ul">,
) => {
  const { parties, onClickParty, ...rest } = addClass(
    props,
    "text-sm max-sm:py-4 max-sm:px-edge",
  );
  if (!parties) return null;
  return (
    <ul {...rest}>
      {parties.map((party) => (
        <li
          key={party.parliamentdotuk}
          className={classes(
            "row hover:bg-surface-hover chip-content pointer-events-auto w-fit cursor-pointer list-none gap-1.5",
            "sm:bg-surface/80",
            "max-sm:chip",
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
