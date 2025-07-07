import Link from "next/link";
import React, { ReactNode } from "react";
import { type ItemTheme as Theme } from "@/api/schema";
import { Optional } from "@/components/optional";
import {
  ItemTheme,
  ItemThemeableProps,
  PartyIconBackground,
  itemThemeCss,
} from "@/features/themed/item-theme";
import type { DivProps, Props } from "@/types/react";
import { addClass } from "@/util/transforms";

const DefaultTheme: Theme = {
  primary: "var(--surface)",
  on_primary: "var(--on-surface)",
  accent: "var(--primary)",
  on_accent: "var(--on-primary)",
};

type HeaderCardProps = DivProps<
  { hero?: ReactNode; inlineImage?: ReactNode } & ItemThemeableProps
>;
export const HeaderCard = (props: HeaderCardProps) => {
  const { inlineImage, hero, children, themeSource, ...rest } = props;

  return (
    <ItemTheme
      themeSource={themeSource}
      {...addClass(
        rest,
        "@container grid card w-full readable grid-cols-[auto_1fr] grid-rows-[auto-auto] surface-primary-tint",
        "[--x-spacing:--spacing(2)] sm:[--x-spacing:--spacing(4)]",
      )}
    >
      <Optional
        value={hero}
        block={(it) => <div className="col-span-full">{it}</div>}
      />

      <div className="grid grid-rows-subgrid grid-cols-subgrid space-x-(--x-spacing) px-(--x-spacing) py-4 col-span-full">
        <Optional value={inlineImage} block={(it) => <>{it}</>} />
        <div className="col-start-2">{children}</div>
      </div>
    </ItemTheme>
  );
};

type ListItemCardProps = Props<
  typeof Link,
  { image?: ReactNode; label?: ReactNode } & ItemThemeableProps
>;
export const ListItemCard = (props: ListItemCardProps) => {
  const { image, children, themeSource, defaultTheme, label, style, ...rest } =
    addClass(
      props,
      "@container max-w-listitem-card card surface-primary-tint-hover block",
    );

  const themedStyle = itemThemeCss(themeSource, defaultTheme, style);

  return (
    <Link style={themedStyle} {...rest}>
      <div className="flex size-full flex-row">
        {image ? (
          <div className="bg-mix-primary-background border-primary m-2 flex aspect-square size-20 shrink-0 flex-col items-start overflow-hidden rounded-md border-1 *:w-full empty:hidden @max-2xs:hidden">
            {image}
          </div>
        ) : (
          <div className="bg-primary h-full w-1" />
        )}

        <div className="w-full p-2 text-sm [&>h2]:text-xl [&>h2]:font-semibold">
          <div className="chip chip-content surface-primary-container float-right w-fit rounded-sm text-xs empty:hidden">
            {label}
          </div>

          {children}
        </div>
      </div>
    </Link>
  );
};

export const ListItemCardVibrant = (props: ListItemCardProps) => {
  const { image, children, themeSource, defaultTheme, label, ...rest } =
    addClass(props, "flex max-w-listitem-card sm:rounded-lg overflow-hidden ");

  return (
    <Link {...rest}>
      <PartyIconBackground
        themeSource={themeSource}
        defaultTheme={defaultTheme === undefined ? DefaultTheme : defaultTheme}
        className="hover-overlay column w-full p-3"
      >
        <div className="flex w-full gap-3">
          <div className="size-16 shrink-0 overflow-hidden rounded-md empty:hidden">
            {image}
          </div>
          <div className="w-full">
            <div className="float-right w-fit text-sm opacity-50">{label}</div>
            <div className="column gap-0.5 text-sm [&>h2]:text-xl [&>h2]:font-semibold">
              {children}
            </div>
          </div>
        </div>
      </PartyIconBackground>
    </Link>
  );
};
