import type { ConstituencyMini } from "@/api";
import { ListItemCard } from "@/components/card";
import { SeparatedRow } from "@/components/collection";
import { OptionalDiv } from "@/components/optional";
import { DateRange } from "@/components/datetime";
import React from "react";
import { navigationHref } from "@/components/models/navigation";

export default function ConstituencyItemCard(props: {
  constituency: ConstituencyMini;
}) {
  const { parliamentdotuk, name, start, end, mp } = props.constituency;

  return (
    <ListItemCard
      href={navigationHref("constituency", parliamentdotuk)}
      party={mp?.party}
    >
      <h2>{name}</h2>

      <SeparatedRow>
        <OptionalDiv value={mp?.party?.name} />
        <OptionalDiv value={mp?.name} />
      </SeparatedRow>

      <DateRange start={start} end={end} />
    </ListItemCard>
  );
}
