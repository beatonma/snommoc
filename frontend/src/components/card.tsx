import React, { ComponentPropsWithoutRef, ReactNode } from "react";
import { addClass } from "@/util/transforms";
import { type PartyTheme } from "@/api";
import {
  PartyIconBackground,
  PartyThemeableProps,
} from "@/components/themed/party";
import Link from "next/link";
import { NextLinkProps } from "@/components/link";
import { Optional } from "@/components/optional";

type CardProps = {
  image?: ReactNode;
} & PartyThemeableProps;

const DefaultTheme: PartyTheme = {
  primary: "var(--surface)",
  on_primary: "var(--on_surface)",
  accent: "var(--primary)",
  on_accent: "var(--on_primary)",
};

type HeaderCardProps = CardProps & ComponentPropsWithoutRef<"div">;
export const HeaderCard = (props: HeaderCardProps) => {
  const { image, children, party, ...rest } = addClass(
    props,
    "@container HeaderCard card surface-alt overflow-hidden w-full readable gap-4",
    "py-2 sm:p-4",
    "sm:rounded-lg sm:min-w-[600px]",
    "grid md:grid-cols-[auto_1fr]",
  );

  return (
    <PartyIconBackground party={party} {...rest}>
      <Optional
        value={image}
        block={(it) => (
          <div className="flex justify-center overflow-hidden md:rounded-lg">
            {it}
          </div>
        )}
      />

      <div className="column max-sm:px-edge">{children}</div>
    </PartyIconBackground>
  );
};

type ListItemCardProps = { label?: string } & CardProps & NextLinkProps;
export const ListItemCard = (props: ListItemCardProps) => {
  const { image, children, party, defaultPartyTheme, label, ...rest } =
    addClass(props, "flex max-w-listitem_card sm:rounded-lg overflow-hidden ");

  return (
    <Link {...rest}>
      <PartyIconBackground
        party={party}
        defaultPartyTheme={
          defaultPartyTheme === undefined ? DefaultTheme : defaultPartyTheme
        }
        className="hover-overlay flex w-full flex-col p-3"
      >
        <div className="flex w-full gap-3">
          {image}
          <div className="w-full">
            <div className="float-right w-fit text-sm opacity-50">{label}</div>
            <div className="flex flex-col gap-0.5 text-sm [&>h2]:text-xl [&>h2]:font-semibold">
              {children}
            </div>
          </div>
        </div>
      </PartyIconBackground>
    </Link>
  );
};
