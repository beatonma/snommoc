import type { Organisation } from "@/api/schema";
import { ListItemCard } from "@/features/cards";
import { navigationHref } from "@/navigation";
import { Props } from "@/types/react";

export const OrganisationItemCard = (
  props: Props<
    typeof ListItemCard,
    { organisation: Organisation },
    "href" | "themeSource"
  >,
) => {
  const { organisation, children, title, ...rest } = props;
  return (
    <ListItemCard
      themeSource={undefined}
      title={title || organisation.name}
      href={navigationHref("organisation", organisation.slug)}
      {...rest}
    >
      <strong>{organisation.name}</strong>
      {children}
    </ListItemCard>
  );
};
