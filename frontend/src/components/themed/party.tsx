import type { Party, PartyDetail, PartyTheme as Theme } from "@/api";
import React from "react";
import { addClass } from "@/util/transforms";
import { Nullish } from "@/types/common";
import { MaskedSvg } from "@/components/image";
import { getOnColor } from "@/components/themed/color";
import { DivProps } from "@/types/react";

type PartyLike = Party | PartyDetail | Theme | Nullish;
export interface PartyThemeableProps {
  party: PartyLike;
  defaultPartyTheme?: Theme | Nullish;
}

const isTheme = (obj: PartyLike): obj is Theme =>
  obj != null && "primary" in obj;

const resolveTheme = (
  obj: PartyLike,
  defaultTheme?: Theme | Nullish,
): Theme | null => {
  if (!obj) return defaultTheme ?? null;
  return isTheme(obj) ? obj : obj.theme;
};

const partySurfaceThemes = (
  party: PartyLike,
  defaultTheme?: Theme | Nullish,
): { primary: React.CSSProperties; accent: React.CSSProperties } | null => {
  const theme = resolveTheme(party, defaultTheme);
  if (!theme) return null;

  const { primary, on_primary, accent, on_accent } = theme;

  // If both components of a theme are CSS variables, use them directly.
  // Otherwise, generate a suitable content color.
  const primaryIsVariable = primary.includes("--") && on_primary.includes("--");
  const accentIsVariable = accent.includes("--") && on_accent.includes("--");

  return {
    primary: {
      backgroundColor: primary,
      color: primaryIsVariable ? on_primary : getOnColor(primary),
    },
    accent: {
      backgroundColor: accent,
      color: accentIsVariable ? on_accent : getOnColor(accent),
    },
  };
};

export const partyColors = (
  party: PartyLike,
  defaultTheme?: Theme | Nullish,
  merge?: object,
): React.CSSProperties => {
  const theme = resolveTheme(party);
  return {
    ...(merge ?? {}),
    ...Object.fromEntries(
      Object.entries({
        "--primary": theme?.primary,
        "--on_primary": getOnColor(theme?.primary),
        "--accent": theme?.accent,
        "--on_accent": getOnColor(theme?.accent),
        accentColor: theme?.primary,
      }).filter(([_, value]) => !!value),
    ),
  };
};

export const PartyTheme = (props: PartyThemeableProps & DivProps) => {
  const { party, children, style, defaultPartyTheme, ...rest } = props;
  const themedStyle = partyColors(party, defaultPartyTheme, style);

  return (
    <div style={{ ...themedStyle }} {...rest}>
      {children}
    </div>
  );
};

export const PartyIconBackground = (props: PartyThemeableProps & DivProps) => {
  const { party, children, style, defaultPartyTheme, ...rest } = props;
  const theme = partySurfaceThemes(party, defaultPartyTheme)?.primary;
  const themedStyle = partyColors(party, defaultPartyTheme, style);

  if (isTheme(party) || (!party?.logo_mask && !party?.logo)) {
    return (
      <div style={{ ...theme, ...themedStyle }} {...rest}>
        {children}
      </div>
    );
  }

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

      {children}
    </div>
  );
};
