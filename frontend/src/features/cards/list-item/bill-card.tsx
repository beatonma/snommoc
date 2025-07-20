import { type Bill } from "@/api/schema";
import { Date } from "@/components/datetime";
import { ListItemCard } from "@/features/cards";
import { navigationHref } from "@/navigation";
import { Props } from "@/types/react";

export const BillItemCard = (
  props: Props<typeof ListItemCard, { bill: Bill }, "href" | "themeSource">,
) => {
  const { bill, children, title, ...rest } = props;
  return (
    <ListItemCard
      themeSource={bill.current_house}
      href={navigationHref("bill", bill.parliamentdotuk)}
      title={title || bill.title}
      {...rest}
    >
      <h1 className="text-base font-bold line-clamp-2">{bill.title}</h1>
      <div className="line-clamp-2">{bill.description}</div>
      <span className="text-sm">
        Updated <Date date={bill.last_update} />
      </span>
      {children}
    </ListItemCard>
  );
};
