import React, { ReactNode } from "react";
import { MemberMiniSchema } from "@/api/schema";
import { OptionalDiv } from "@/components/optional";
import { SeparatedRow } from "@/components/row";
import { ListItemCard } from "@/features/cards";
import { MemberPortrait } from "@/features/member-portrait";
import { ItemThemeableProps } from "@/features/themed/item-theme";
import { navigationHref } from "@/navigation";
import { ChildrenProps, ClassNameProps } from "@/types/common";

interface MemberItemProps {
  member: Partial<MemberMiniSchema> &
    Pick<MemberMiniSchema, "parliamentdotuk" | "name">;
  badge?: ReactNode;
  label?: ReactNode;
  image?: ReactNode;
  showParty?: boolean;
  showConstituency?: boolean;
  usePartyTheme?: boolean;
}

export const MemberItemCard = (
  props: MemberItemProps &
    Pick<ItemThemeableProps, "defaultTheme"> &
    ChildrenProps &
    ClassNameProps,
) => {
  const {
    member,
    showParty,
    showConstituency,
    image,
    badge,
    children,
    usePartyTheme = true,
    ...rest
  } = props;

  return (
    <ListItemCard
      href={navigationHref("person", member.parliamentdotuk)}
      themeSource={usePartyTheme ? member.party : null}
      image={
        <div className="relative size-full">
          {image ?? <MemberPortrait name={member.name} src={member.portrait} />}
          <div className="absolute bottom-0 right-0 m-1">{badge}</div>
        </div>
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
      {children}
    </ListItemCard>
  );
};
