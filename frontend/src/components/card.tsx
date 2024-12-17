import React, { ComponentPropsWithoutRef, ReactNode } from "react";
import { addClass } from "@/util/transforms";
import { Party, PartyDetail } from "@/api";
import { PartyIconBackground } from "@/components/themed/party";
import Link from "next/link";
import { NextLinkProps } from "@/components/link";
import { Optional } from "@/components/optional";

type CardProps = {
  image?: ReactNode;
  party?: Party | PartyDetail | null;
};

type HeaderCardProps = CardProps & ComponentPropsWithoutRef<"div">;
export const HeaderCard = (props: HeaderCardProps) => {
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
      <Optional
        value={image}
        block={(it) => (
          <div className="flex w-full justify-center self-center overflow-hidden rounded-lg sm:w-auto">
            {it}
          </div>
        )}
      />

      <div className="flex flex-col gap-1">{children}</div>
    </>
  );

  return (
    <PartyIconBackground party={party} {...rest}>
      {content}
    </PartyIconBackground>
  );
};

type ListItemCardProps = { label?: string } & CardProps & NextLinkProps;
export const ListItemCard = (props: ListItemCardProps) => {
  const { image, children, party, label, ...rest } = addClass(
    props,
    "flex max-w-[400px]",
    "hover-overlay",
  );

  return (
    <Link {...rest}>
      <PartyIconBackground
        party={party}
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
