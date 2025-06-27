import React from "react";
import type { ConstituencyMini } from "@/api";
import { DateRange } from "@/components/datetime";
import { OptionalDiv } from "@/components/optional";
import { SeparatedRow } from "@/components/row";
import { ListItemCard } from "@/features/cards";
import { navigationHref } from "@/navigation";

export const ConstituencyItemCard = (props: {
  constituency: ConstituencyMini;
}) => {
  const { parliamentdotuk, name, start, end, mp } = props.constituency;

  return (
    <ListItemCard
      href={navigationHref("constituency", parliamentdotuk)}
      themeSource={mp?.party}
    >
      <h2>{name}</h2>

      <SeparatedRow>
        <OptionalDiv value={mp?.party?.name} />
        <OptionalDiv value={mp?.name} />
      </SeparatedRow>

      <DateRange start={start} end={end} />
    </ListItemCard>
  );
};
