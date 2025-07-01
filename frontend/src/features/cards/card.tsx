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

type CardProps = {
  image?: ReactNode;
} & ItemThemeableProps;

const DefaultTheme: Theme = {
  primary: "var(--surface)",
  on_primary: "var(--on-surface)",
  accent: "var(--primary)",
  on_accent: "var(--on-primary)",
};

type HeaderCardProps = DivProps<CardProps>;
export const HeaderCard = (props: HeaderCardProps) => {
  const { image, children, themeSource, ...rest } = addClass(
    props,
    "@container card overflow-hidden w-full readable gap-4",
    "py-2 sm:p-4",
    "sm:rounded-lg sm:min-w-[600px]",
    "grid md:grid-cols-[auto_1fr] surface-primary-tint",
  );

  return (
    <ItemTheme themeSource={themeSource} {...rest}>
      <Optional
        value={image}
        block={(it) => (
          <div className="flex justify-center overflow-hidden md:rounded-lg">
            {it}
          </div>
        )}
      />

      <div className="column max-sm:px-edge">{children}</div>
    </ItemTheme>
  );
};

type ListItemCardProps = Props<typeof Link, { label?: ReactNode } & CardProps>;
export const ListItemCard = (props: ListItemCardProps) => {
  const { image, children, themeSource, defaultTheme, label, style, ...rest } =
    addClass(
      props,
      "@container max-w-listitem-card card surface-primary-tint-hover",
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
          <div className="chip chip-content bg-primary/60 text-on-primary float-right w-fit rounded-sm text-xs empty:hidden">
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
