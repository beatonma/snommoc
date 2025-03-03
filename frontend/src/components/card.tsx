import React, { ComponentPropsWithoutRef, ReactNode } from "react";
import { addClass } from "@/util/transforms";
import { type PartyTheme as Theme } from "@/api";
import {
  partyColors,
  PartyIconBackground,
  PartyTheme,
  PartyThemeableProps,
} from "@/components/themed/party";
import Link from "next/link";
import { NextLinkProps } from "@/components/link";
import { Optional } from "@/components/optional";

type CardProps = {
  image?: ReactNode;
} & PartyThemeableProps;

const DefaultTheme: Theme = {
  primary: "var(--surface)",
  on_primary: "var(--on_surface)",
  accent: "var(--primary)",
  on_accent: "var(--on_primary)",
};

type HeaderCardProps = CardProps & ComponentPropsWithoutRef<"div">;
export const HeaderCard = (props: HeaderCardProps) => {
  const { image, children, party, ...rest } = addClass(
    props,
    "@container card surface-alt overflow-hidden w-full readable gap-4",
    "py-2 sm:p-4",
    "sm:rounded-lg sm:min-w-[600px]",
    "grid md:grid-cols-[auto_1fr] surface-primary-tint",
  );

  return (
    <PartyTheme party={party} {...rest}>
      <Optional
        value={image}
        block={(it) => (
          <div className="flex justify-center overflow-hidden md:rounded-lg">
            {it}
          </div>
        )}
      />

      <div className="column max-sm:px-edge">{children}</div>
    </PartyTheme>
  );
};

type ListItemCardProps = { label?: string } & CardProps & NextLinkProps;
export const ListItemCard = (props: ListItemCardProps) => {
  const { image, children, party, defaultPartyTheme, label, style, ...rest } =
    addClass(
      props,
      "@container max-w-listitem_card card surface-primary-tint-hover",
    );

  const themedStyle = partyColors(party, defaultPartyTheme, style);

  return (
    <Link style={themedStyle} {...rest}>
      <div className="flex size-full flex-row">
        {image ? (
          <div className="bg-mix_primary_background border-primary m-2 flex aspect-square size-20 shrink-0 flex-col items-start overflow-hidden rounded-md border-1 *:w-full empty:hidden @max-sm:hidden">
            {image}
          </div>
        ) : (
          <div className="bg-primary h-full w-1" />
        )}

        <div className="w-full p-2 text-sm [&>h2]:text-xl [&>h2]:font-semibold">
          <div className="chip chip-content bg-primary/60 text-on_primary float-right w-fit rounded-sm text-xs empty:hidden">
            {label}
          </div>

          {children}
        </div>
      </div>
    </Link>
  );
};

export const ListItemCardVibrant = (props: ListItemCardProps) => {
  const { image, children, party, defaultPartyTheme, label, ...rest } =
    addClass(props, "flex max-w-listitem_card sm:rounded-lg overflow-hidden ");

  return (
    <Link {...rest}>
      <PartyIconBackground
        party={party}
        defaultPartyTheme={
          defaultPartyTheme === undefined ? DefaultTheme : defaultPartyTheme
        }
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
// export const ListItemCard = ListItemCardVibrant;
