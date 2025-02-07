import { MemberMiniSchema } from "@/api";
import { ListItemCard } from "@/components/card";
import { MemberPortrait } from "@/components/member-portrait";
import { OptionalDiv } from "@/components/optional";
import { SeparatedRow } from "@/components/collection";
import React from "react";
import { ClassNameProps } from "@/types/common";
import { PartyThemeableProps } from "@/components/themed/party";

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
export const MemberItem = (
  props: MemberItemProps &
    Pick<PartyThemeableProps, "defaultPartyTheme"> &
    ClassNameProps,
) => {
  const {
    member,
    showParty,
    showConstituency,
    usePartyTheme = true,
    ...rest
  } = props;

  return (
    <ListItemCard
      href={`/members/${member.parliamentdotuk}/`}
      party={usePartyTheme ? member.party : null}
      title={`${member.parliamentdotuk}`}
      image={
        <MemberPortrait
          name={member.name}
          src={member.portrait}
          className="size-16 shrink-0 overflow-hidden rounded-md"
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
