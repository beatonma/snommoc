import type { Party, PartyDetail, PartyTheme } from "@/api";
import React, { ComponentPropsWithoutRef } from "react";
import { addClass } from "@/util/transforms";
import { Nullish } from "@/types/common";
import { MaskedSvg } from "@/components/image";

interface PartyProps {
  party: Party | PartyDetail | null | undefined;
}

export const rgb = (value: string | undefined) => {
  if (value?.match(/^\d+ \d+ \d+$/)) return `rgb(${value})`;
  return value;
};

const DefaultTheme: PartyTheme = {
  primary: "var(--surface)",
  on_primary: "var(--on_surface)",
  accent: "var(--primary)",
  on_accent: "var(--on_primary)",
};

const partyTheme = (party: Party | PartyDetail | Nullish) => {
  const theme = party?.theme ?? DefaultTheme;

  return {
    primary: {
      backgroundColor: rgb(theme?.primary),
      color: getOnColor(theme?.primary),
    },
    accent: {
      backgroundColor: rgb(theme?.accent),
      color: getOnColor(theme?.accent),
    },
  };
};

const getOnColor = (
  backgroundColorRgb: string | undefined,
): string | undefined => {
  if (!backgroundColorRgb) return undefined;

  const components = backgroundColorRgb
    .match(/^(\d+),? (\d+),? (\d+)$/)
    ?.slice(1);
  if (!components || !components.length) return undefined;
  const mean =
    components.reduce((acc, it) => parseInt(it) + acc, 0) / components.length;
  const mixer = mean > 127 ? "black" : "white";

  return `color-mix(in srgb, rgb(${backgroundColorRgb}) 10%, ${mixer})`;
};
export const partyStyle = (party: Party | PartyDetail | Nullish) => {
  const theme = party?.theme;
  return Object.fromEntries(
    Object.entries({
      "--primary": rgb(theme?.primary),
      "--on_primary": getOnColor(theme?.primary),
      "--accent": rgb(theme?.accent),
      "--on_accent": getOnColor(theme?.accent),
      accentColor: rgb(theme?.primary),
    }).filter(([_, value]) => !!value),
  );
};

export const PartyIconBackground = (
  props: PartyProps & ComponentPropsWithoutRef<"div">,
) => {
  const { party, children, style, ...rest } = props;
  // const style = partyStyle(party)
  const theme = partyTheme(party);

  const themedStyle = {
    ...style,
    ...partyStyle(party),
  };

  if (!party?.logo)
    return (
      <div style={{ ...theme.primary, ...themedStyle }} {...rest}>
        {children}
      </div>
    );

  return (
    <div
      style={{
        ...themedStyle,
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
