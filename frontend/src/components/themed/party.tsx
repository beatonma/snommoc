import type { Party, PartyDetail, PartyTheme } from "@/api";
import React, { ComponentPropsWithoutRef } from "react";
import { addClass } from "@/util/transforms";
import { Nullish } from "@/types/common";
import { MaskedSvg } from "@/components/image";
import { getOnColor } from "@/components/themed/color";

type PartyLike = Party | PartyDetail | Nullish;
export interface PartyThemeableProps {
  party: PartyLike;
  defaultPartyTheme?: PartyTheme | Nullish;
}

const partySurfaceThemes = (
  party: PartyLike,
  defaultTheme?: PartyTheme | Nullish,
): { primary: React.CSSProperties; accent: React.CSSProperties } | null => {
  const theme = party?.theme ?? (defaultTheme === null ? null : defaultTheme);
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
  merge?: object,
): React.CSSProperties => {
  const theme = party?.theme;
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
