import React from "react";
import { MemberMiniSchema } from "@/api";
import { ListItemCard } from "@/components/card";
import { SeparatedRow } from "@/components/collection";
import { MemberPortrait } from "@/components/models/member-portrait";
import { OptionalDiv } from "@/components/optional";
import { PartyThemeableProps } from "@/components/themed/party";
import { navigationHref } from "@/navigation";
import { ClassNameProps } from "@/types/common";

type OptionalMemberFields = Pick<
  Partial<MemberMiniSchema>,
  "current_posts" | "constituency"
>;
type MemberLike = Omit<MemberMiniSchema, keyof OptionalMemberFields> &
  OptionalMemberFields;

interface MemberItemProps {
  member: MemberLike;
  label?: string;
  showParty?: boolean;
  showConstituency?: boolean;
  usePartyTheme?: boolean;
}

export default function MemberItemCard(
  props: MemberItemProps &
    Pick<PartyThemeableProps, "defaultPartyTheme"> &
    ClassNameProps,
) {
  const {
    member,
    showParty,
    showConstituency,
    usePartyTheme = true,
    ...rest
  } = props;

  return (
    <ListItemCard
      href={navigationHref("person", member.parliamentdotuk)}
      party={usePartyTheme ? member.party : null}
      image={<MemberPortrait name={member.name} src={member.portrait} />}
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
}
