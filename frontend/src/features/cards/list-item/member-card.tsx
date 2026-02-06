import React, { ReactNode } from "react";
import { MemberMiniSchema } from "@/api/schema";
import { OptionalDiv, onlyIf } from "@/components/optional";
import { SeparatedRow } from "@/components/row";
import { ListItemCard } from "@/features/cards";
import { MemberPortrait } from "@/features/member-portrait";
import { ItemThemeableProps } from "@/features/themed/item-theme";
import { navigationHref } from "@/navigation";
import { DivPropsNoChildren, Props } from "@/types/react";
import { addClass } from "@/util/transforms";

type Member = Partial<MemberMiniSchema> &
  Pick<MemberMiniSchema, "parliamentdotuk" | "name">;
interface MemberItemProps {
  member: Member;
  badge?: ReactNode;
  label?: ReactNode;
  image?: ReactNode;
  showParty?: boolean;
  showConstituency?: boolean;
  usePartyTheme?: boolean;
  layout?: "inline" | "hero";
}

export const MemberItemCard = (
  props: Props<
    typeof ListItemCard,
    MemberItemProps & Pick<ItemThemeableProps, "defaultTheme">,
    "href" | "themeSource"
  >,
) => {
  const {
    member,
    showParty = true,
    showConstituency = true,
    image,
    badge,
    children,
    layout = "inline",
    usePartyTheme = true,
    ...rest
  } = props;

  const partyAndConstituency = [
    onlyIf(showParty, member.party?.name),
    onlyIf(showConstituency, member.constituency?.name),
  ]
    .filter(Boolean)
    .join(", ");

  return (
    <ListItemCard
      href={navigationHref("person", member.parliamentdotuk)}
      themeSource={usePartyTheme ? member.party : null}
      hero={onlyIf(
        layout === "hero",
        <CardImage
          member={member}
          badge={badge}
          image={
            image ?? (
              <MemberPortrait
                name={member.name}
                src={member.portrait?.fullsize_url}
                aspect="aspect-wide"
                className="object-top"
                width={400}
              />
            )
          }
        />,
      )}
      inlineImage={onlyIf(
        layout === "inline",
        <CardImage
          member={member}
          badge={badge}
          image={
            image ?? (
              <MemberPortrait
                name={member.name}
                src={member.portrait?.square_url}
                aspect="aspect-square"
                width="parliament-thumbnail"
              />
            )
          }
        />,
      )}
      {...rest}
    >
      <h2>{member.name}</h2>
      <OptionalDiv
        title="Current post"
        value={member.current_posts}
        className="line-clamp-1"
      />

      <OptionalDiv className="line-clamp-1" value={partyAndConstituency} />

      {children}
    </ListItemCard>
  );
};

const CardImage = (
  props: DivPropsNoChildren<
    Pick<MemberItemProps, "member" | "image" | "badge">
  >,
) => {
  const { member, image, badge, ...rest } = props;
  return (
    <div {...addClass(rest, "relative")}>
      {image}
      <div className="absolute bottom-0 right-0 m-1">{badge}</div>
    </div>
  );
};
