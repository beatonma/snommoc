import { Division, HouseType, ItemTheme } from "@/api/schema";
import { Date } from "@/components/datetime";
import Icon, { IconProps } from "@/components/icon";
import { onlyIf } from "@/components/optional";
import { SeparatedRow } from "@/components/row";
import { ListItemCard } from "@/features/cards";
import { HouseLink } from "@/features/linked-data";
import { navigationHref } from "@/navigation";
import { Props } from "@/types/react";

const HouseTheme = (house: HouseType): ItemTheme => {
  return {
    Commons: {
      primary: "var(--color-house-commons)",
      on_primary: "var(--color-house-on-commons)",
      accent: "var(--color-house-commons)",
      on_accent: "var(--color-house-on-commons)",
    },
    Lords: {
      primary: "var(--color-house-lords)",
      on_primary: "var(--color-house-on-lords)",
      accent: "var(--color-house-lords)",
      on_accent: "var(--color-house-on-lords)",
    },
  }[house];
};

export const DivisionItemCard = (
  props: Props<
    typeof ListItemCard,
    { division: Division; showPassedImage?: boolean },
    "themeSource" | "href"
  >,
) => {
  const { division, showPassedImage = true, children, title, ...rest } = props;

  return (
    <ListItemCard
      themeSource={HouseTheme(division.house)}
      href={navigationHref(
        "division",
        division.house,
        division.parliamentdotuk,
      )}
      title={title || division.title}
      inlineImage={onlyIf(
        showPassedImage,
        <PassIcon
          isPassed={division.is_passed}
          className="p-4 fill-current size-full"
        />,
      )}
      {...rest}
    >
      <h1 className="text-base font-bold line-clamp-2">{division.title}</h1>
      <SeparatedRow>
        <Date date={division.date} />
        <HouseLink house={division.house} showDot={false} longFormat={true} />
      </SeparatedRow>
      {children}
    </ListItemCard>
  );
};

const PassIcon = (props: { isPassed: boolean } & Omit<IconProps, "icon">) => {
  const { isPassed, ...rest } = props;
  return <Icon icon={isPassed ? "Check" : "Close"} {...rest} />;
};
