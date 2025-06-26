import React from "react";
import type { ItemTheme as LocalTheme, Party, PartyDetail } from "@/api";
import { MaskedSvg } from "@/components/image";
import { getOnColor } from "@/components/themed/color";
import { Nullish } from "@/types/common";
import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

type ItemThemeProvider =
  | { theme: LocalTheme | Nullish }
  | Party
  | PartyDetail
  | LocalTheme
  | Nullish;
export interface ItemThemeableProps {
  themeSource: ItemThemeProvider;
  defaultTheme?: LocalTheme | Nullish;
}

const isTheme = (obj: ItemThemeProvider): obj is LocalTheme =>
  obj != null && "primary" in obj;
const isPartyLike = (obj: ItemThemeProvider): obj is Party | PartyDetail =>
  obj != null && "logo" in obj;

const resolveTheme = (
  obj: ItemThemeProvider,
  defaultTheme?: LocalTheme | Nullish,
): LocalTheme | null => {
  if (!obj) return defaultTheme ?? null;
  return isTheme(obj) ? obj : (obj.theme ?? null);
};

const itemSurfaceThemes = (
  themeSource: ItemThemeProvider,
  defaultTheme?: LocalTheme | Nullish,
): { primary: React.CSSProperties; accent: React.CSSProperties } | null => {
  const theme = resolveTheme(themeSource, defaultTheme);
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

export const itemThemeCss = (
  themeSource: ItemThemeProvider,
  defaultTheme?: LocalTheme | Nullish,
  merge?: object,
): React.CSSProperties => {
  const theme = resolveTheme(themeSource, defaultTheme);
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

export const ItemTheme = (props: DivProps<ItemThemeableProps>) => {
  const { themeSource, children, style, defaultTheme, ...rest } = props;
  const themedStyle = itemThemeCss(themeSource, defaultTheme, style);

  return (
    <div style={{ ...themedStyle }} {...rest}>
      {children}
    </div>
  );
};

export const PartyIconBackground = (props: DivProps<ItemThemeableProps>) => {
  const {
    themeSource: themeSource,
    children,
    style,
    defaultTheme,
    ...rest
  } = props;
  const theme = itemSurfaceThemes(themeSource, defaultTheme)?.primary;
  const themedStyle = itemThemeCss(themeSource, defaultTheme, style);

  if (
    !isPartyLike(themeSource) ||
    (!themeSource?.logo_mask && !themeSource?.logo)
  ) {
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
        src={themeSource.logo_mask ?? themeSource.logo}
        className="absolute inset-0 size-full translate-x-1/2 bg-black/[0.08]"
      />

      {children}
    </div>
  );
};
