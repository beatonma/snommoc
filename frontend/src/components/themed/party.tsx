import type { Party, PartyDetail } from "@/api";
import React, { ComponentPropsWithoutRef } from "react";
import { classes } from "@/util/transforms";
import { ThemedDiv } from "@/components/themed/themed-div";
import { Nullish } from "@/types/common";
import { MaskedSvg } from "@/components/image";

interface PartyProps {
  party: Party | PartyDetail | null | undefined;
}

export const rgb = (value: string | undefined) =>
  value ? `rgb(${value})` : undefined;

const partyTheme = (party: Party | PartyDetail) => ({
  primary: {
    backgroundColor: rgb(party.theme?.primary),
    color: rgb(party.theme?.on_primary),
  },
  accent: {
    backgroundColor: rgb(party.theme?.accent),
    color: rgb(party.theme?.on_accent),
  },
});

export const partyThemeVariableStyle = (
  party: Party | PartyDetail | Nullish,
) => {
  if (!party) return {};
  return Object.fromEntries(
    Object.entries({
      primary: party.theme?.primary,
      on_primary: party.theme?.on_primary,
      accent: party.theme?.accent,
      on_accent: party.theme?.on_accent,
    })
      .filter(([key, value]) => !!value)
      .map(([key, value]) => [`--${key}`, value]),
  );
};

/**
 * Container with party primary theme.
 */
export const PartyPrimary = (
  props: PartyProps & ComponentPropsWithoutRef<"div">,
) => {
  const { party, ...rest } = props;
  if (!party) return <div {...rest} />;

  return <ThemedDiv theme={partyTheme(party).primary} {...rest} />;
};

/**
 * Container with party accent theme.
 */
export const PartyAccent = (
  props: PartyProps & ComponentPropsWithoutRef<"div">,
) => {
  const { party, ...rest } = props;
  if (!party) return <div {...rest} />;

  return <ThemedDiv theme={partyTheme(party).accent} {...rest} />;
};

export const PartyIconBackground = (
  props: PartyProps & ComponentPropsWithoutRef<"div">,
) => {
  const { party, className, children, ...rest } = props;
  if (!party)
    return (
      <div className={className} {...rest}>
        {children}
      </div>
    );
  if (!party?.logo)
    return (
      <PartyPrimary party={party} className={className} {...rest}>
        {children}
      </PartyPrimary>
    );

  const theme = partyTheme(party);

  return (
    <div
      className={classes(className, "relative overflow-hidden")}
      style={{
        color: theme.primary.color,
      }}
      {...rest}
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
