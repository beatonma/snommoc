import React, { ComponentPropsWithoutRef, ReactNode } from "react";
import { addClass } from "@/util/transforms";
import { Party, PartyDetail } from "@/api";
import { PartyIconBackground } from "@/components/themed/party";
import Link from "next/link";
import { NextLinkProps } from "@/components/link";

type CardProps = {
  image?: ReactNode;
  party?: Party | PartyDetail | null;
};

export const HeaderCard = (
  props: CardProps & ComponentPropsWithoutRef<"div">,
) => {
  const { image, children, party, ...rest } = addClass(
    props,
    "flex flex-col sm:flex-row",
    "sm:rounded-lg",
    "gap-4 p-2 sm:p-4",
    "sm:rounded-lg overflow-hidden",
    "w-full sm:w-fit sm:min-w-[600px] readable",
  );

  const content = (
    <>
      <div className="self-center overflow-hidden rounded-lg">{image}</div>
      <div className="flex flex-col gap-1">{children}</div>
    </>
  );

  return (
    <PartyIconBackground party={party} {...rest}>
      {content}
    </PartyIconBackground>
  );
};

export const ListItemCard = (props: CardProps & NextLinkProps) => {
  const { image, children, party, ...rest } = addClass(props, "flex");

  return (
    <Link {...rest}>
      <PartyIconBackground
        party={party}
        className="flex w-full gap-3 overflow-hidden p-3 sm:rounded-lg"
      >
        {image}
        <div className="flex flex-col gap-0.5 text-sm [&>h2]:text-xl [&>h2]:font-semibold">
          {children}
        </div>
      </PartyIconBackground>
    </Link>
  );
};
