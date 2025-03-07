import React, { ComponentPropsWithoutRef } from "react";
import { Party } from "@/api";
import { ListItemCard } from "@/components/card";
import { OptionalSvg } from "@/components/image";
import { onlyIf } from "@/components/optional";
import { navigationHref } from "@/navigation";
import { plural } from "@/util/plurals";

export default function PartyItemCard(
  props: { party: Party } & ComponentPropsWithoutRef<"a">,
) {
  const { party, className, ...rest } = props;

  return (
    <ListItemCard
      href={navigationHref("party", party.parliamentdotuk)}
      themeSource={party}
      defaultTheme={{
        primary: "var(--surface)",
        on_primary: "var(--on_surface)",
        accent: "var(--surface)",
        on_accent: "var(--on_surface)",
      }}
      image={onlyIf(
        party.logo,
        <OptionalSvg
          src={party.logo}
          alt={party.name}
          className="bg-light_surface/75 p-2"
        />,
      )}
      {...rest}
    >
      <h2>{party.name}</h2>

      <span>{partyMemberSummary(party)}</span>
    </ListItemCard>
  );
}

const partyMemberSummary = (party: Party) => {
  const mps = party.active_commons_members;
  const lords = party.active_member_count - (party.active_commons_members ?? 0);

  const parts = [];
  if (mps) parts.push(plural("MP", mps));
  if (lords) parts.push(plural("Lord", lords));

  return parts.join(", ");
};
