import type { MemberMiniSchema } from "@/api";
import { ListItemCard } from "@/components/card";
import { MemberPortrait } from "@/components/member-portrait";
import { OptionalDiv } from "@/components/optional";
import { SeparatedRow } from "@/components/collection";
import React from "react";
import { ClassNameProps } from "@/types/common";

interface MemberItemProps {
  member: MemberMiniSchema;
  label?: string;
  showParty?: boolean;
  showConstituency?: boolean;
}
export const MemberItem = (props: MemberItemProps & ClassNameProps) => {
  const { member, label, showParty, showConstituency, ...rest } = props;
  return (
    <ListItemCard
      href={`/members/${member.parliamentdotuk}/`}
      party={member.party}
      label={label}
      title={`${member.parliamentdotuk}`}
      image={
        <MemberPortrait
          name={member.name}
          src={member.portrait}
          className="size-16 shrink-0 overflow-hidden rounded-md bg-primary-900"
        />
      }
      {...rest}
    >
      <h2>{member.name}</h2>
      <OptionalDiv
        title="Current post"
        value={member.current_posts}
        className="line-clamp-1"
      />
      <SeparatedRow>
        <OptionalDiv
          title="Party"
          value={member.party?.name}
          condition={() => showParty !== false}
          className="line-clamp-1"
        />
        <OptionalDiv
          title="Constituency"
          value={member.constituency?.name}
          condition={() => showConstituency !== false}
          className="line-clamp-1"
        />
      </SeparatedRow>
    </ListItemCard>
  );
};
