import React from "react";
import { Party } from "@/api/schema";
import { OptionalSvg } from "@/components/image";
import { onlyIf } from "@/components/optional";
import { ListItemCard } from "@/features/cards";
import { navigationHref } from "@/navigation";
import { Props } from "@/types/react";
import { plural } from "@/util/plurals";

export const PartyItemCard = (props: Props<"a", { party: Party }>) => {
  const { party, className, ...rest } = props;

  return (
    <ListItemCard
      href={navigationHref("party", party.parliamentdotuk)}
      themeSource={party}
      inlineImage={onlyIf(
        party.logo,
        <OptionalSvg
          src={party.logo}
          alt={party.name}
          className="bg-white/75 p-2"
        />,
      )}
      {...rest}
    >
      <h2>{party.name}</h2>

      <span>{partyMemberSummary(party)}</span>
    </ListItemCard>
  );
};

const partyMemberSummary = (party: Party) => {
  const mps = party.active_commons_members;
  const lords = party.active_member_count - (party.active_commons_members ?? 0);

  const parts = [];
  if (mps) parts.push(plural("MP", mps));
  if (lords) parts.push(plural("Lord", lords));

  return parts.join(", ");
};
