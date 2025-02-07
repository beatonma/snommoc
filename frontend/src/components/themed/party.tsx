import type { Party, PartyDetail, PartyTheme } from "@/api";
import React, { ComponentPropsWithoutRef } from "react";
import { addClass } from "@/util/transforms";
import { Nullish } from "@/types/common";
import { MaskedSvg } from "@/components/image";

type PartyLike = Party | PartyDetail | Nullish;
export interface PartyThemeableProps {
  party: PartyLike;
  defaultPartyTheme?: PartyTheme | Nullish;
}

export const rgb = (value: string | undefined) => {
  if (value?.match(/^\d+,? \d+,? \d+$/)) return `rgb(${value})`;
  return value;
};

const partySurfaceThemes = (
  party: PartyLike,
  defaultTheme?: PartyTheme | Nullish,
): { primary: React.CSSProperties; accent: React.CSSProperties } | null => {
  const theme = party?.theme ?? (defaultTheme === null ? null : defaultTheme);
  if (!theme) return null;

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

export const partyColors = (
  party: PartyLike,
  merge?: object,
): React.CSSProperties => {
  const theme = party?.theme;
  return {
    ...(merge ?? {}),
    ...Object.fromEntries(
      Object.entries({
        "--primary": rgb(theme?.primary),
        "--on_primary": getOnColor(theme?.primary),
        "--accent": rgb(theme?.accent),
        "--on_accent": getOnColor(theme?.accent),
        accentColor: rgb(theme?.primary),
      }).filter(([_, value]) => !!value),
    ),
  };
};

export const PartyIconBackground = (
  props: PartyThemeableProps & ComponentPropsWithoutRef<"div">,
) => {
  const { party, children, style, defaultPartyTheme, ...rest } = props;
  const theme = partySurfaceThemes(party, defaultPartyTheme)?.primary;
  const themedStyle = partyColors(party, style);

  if (!party?.logo_mask && !party?.logo)
    return (
      <div style={{ ...theme, ...themedStyle }} {...rest}>
        {children}
      </div>
    );
  return (
    <div
      style={{
        ...themedStyle,
        ...theme,
      }}
      {...addClass(rest, "relative overflow-hidden")}
    >
      <MaskedSvg
        src={party.logo_mask ?? party.logo}
        className="absolute inset-0 size-full translate-x-1/2 bg-black/[0.08]"
      />

      <div className="relative">{children}</div>
    </div>
  );
};
