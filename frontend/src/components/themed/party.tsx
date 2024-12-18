import type { Party, PartyDetail, PartyTheme } from "@/api";
import React, { ComponentPropsWithoutRef } from "react";
import { addClass } from "@/util/transforms";
import { Nullish } from "@/types/common";
import { MaskedSvg } from "@/components/image";

interface PartyProps {
  party: Party | PartyDetail | null | undefined;
}

export const rgb = (value: string | undefined) =>
  value ? `rgb(${value})` : undefined;

const DefaultTheme: PartyTheme = {
  primary: "var(--primary)",
  on_primary: "var(--on_primary)",
  accent: "var(--accent)",
  on_accent: "var(--on_accent)",
};

const partyTheme = (party: Party | PartyDetail | Nullish) => {
  const theme = party?.theme ?? DefaultTheme;

  return {
    primary: {
      backgroundColor: rgb(theme?.primary),
      color: rgb(theme?.on_primary),
    },
    accent: {
      backgroundColor: rgb(theme?.accent),
      color: rgb(theme?.on_accent),
    },
  };
};

export const partyStyle = (party: Party | PartyDetail | Nullish) => {
  const theme = party?.theme;
  return Object.fromEntries(
    Object.entries({
      primary: theme?.primary,
      on_primary: theme?.on_primary,
      accent: theme?.accent,
      on_accent: theme?.on_accent,
    })
      .filter(([_, value]) => !!value)
      .map(([key, value]) => [`--${key}`, value]),
  );
};

export const PartyIconBackground = (
  props: PartyProps & ComponentPropsWithoutRef<"div">,
) => {
  const { party, children, ...rest } = props;
  const theme = partyTheme(party);

  if (!party?.logo)
    return (
      <div
        style={{
          color: theme.primary.color,
          backgroundColor: theme.primary.backgroundColor,
        }}
        {...rest}
      >
        {children}
      </div>
    );

  return (
    <div
      style={{
        color: theme.primary.color,
      }}
      {...addClass(rest, "relative overflow-hidden")}
    >
      <div
        className="absolute inset-0 z-[-1] size-full"
        style={{
          backgroundColor: theme.primary.backgroundColor,
        }}
      >
        <MaskedSvg
          src={party.logo_mask ?? party.logo}
          className="inset-0 size-full translate-x-1/2 bg-black/[0.08]"
        />
      </div>
      {children}
    </div>
  );
};
