import { Division, HouseType, ItemTheme } from "@/api/schema";
import { Date } from "@/components/datetime";
import Icon, { IconProps } from "@/components/icon";
import { SeparatedRow } from "@/components/row";
import { ListItemCard } from "@/features/cards";
import { HouseLink } from "@/features/linked-data";
import { navigationHref } from "@/navigation";
import { ClassNameProps } from "@/types/common";

const HouseTheme = (house: HouseType): ItemTheme => {
  return {
    Commons: {
      primary: "var(--color-house_commons)",
      on_primary: "var(--color-house_on_commons)",
      accent: "var(--color-house_commons)",
      on_accent: "var(--color-house_on_commons)",
    },
    Lords: {
      primary: "var(--color-house_lords)",
      on_primary: "var(--color-house_on_lords)",
      accent: "var(--color-house_lords)",
      on_accent: "var(--color-house_on_lords)",
    },
  }[house];
};

export const DivisionItemCard = (
  props: { division: Division } & ClassNameProps,
) => {
  const { division, ...rest } = props;

  return (
    <ListItemCard
      themeSource={HouseTheme(division.house)}
      href={navigationHref(
        "division",
        division.house,
        division.parliamentdotuk,
      )}
      title={division.title}
      image={
        <PassIcon
          isPassed={division.is_passed}
          className="p-4 fill-current size-full"
        />
      }
      {...rest}
    >
      <h1 className="text-base font-bold line-clamp-2">{division.title}</h1>
      <SeparatedRow>
        <Date date={division.date} />
        <HouseLink house={division.house} showDot={false} longFormat={true} />
      </SeparatedRow>
    </ListItemCard>
  );
};

const PassIcon = (props: { isPassed: boolean } & Omit<IconProps, "icon">) => {
  const { isPassed, ...rest } = props;
  return <Icon icon={isPassed ? "Check" : "Close"} {...rest} />;
};
