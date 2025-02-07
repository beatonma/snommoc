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
    "flex flex-col sm:flex-row",
    "sm:rounded-lg",
    "gap-4 p-2 sm:p-4",
    "sm:rounded-lg overflow-hidden",
    "w-full sm:min-w-[600px] readable",
  );

  return (
    <PartyIconBackground party={party} {...rest}>
      <Optional
        value={image}
        block={(it) => (
          <div className="flex w-full justify-center self-center overflow-hidden rounded-lg sm:w-auto">
            {it}
          </div>
        )}
      />

      <div className="flex flex-col gap-1">{children}</div>
    </PartyIconBackground>
  );
};

type ListItemCardProps = { label?: string } & CardProps & NextLinkProps;
export const ListItemCard = (props: ListItemCardProps) => {
  const { image, children, party, defaultPartyTheme, label, ...rest } =
    addClass(props, "flex max-w-listitem_card", "hover-overlay");

  return (
    <Link {...rest}>
      <PartyIconBackground
        party={party}
        defaultPartyTheme={
          defaultPartyTheme === undefined ? DefaultTheme : defaultPartyTheme
        }
        className="flex w-full flex-col overflow-hidden p-3 sm:rounded-lg"
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
