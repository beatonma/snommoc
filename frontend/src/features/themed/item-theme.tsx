import React from "react";
import type { ItemTheme as LocalTheme, Party, PartyDetail } from "@/api/schema";
import { MaskedSvg } from "@/components/image";
import { getContainerColor, getOnColor } from "@/features/themed/color";
import { Nullish } from "@/types/common";
import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

type ItemThemeProvider = { theme: LocalTheme | Nullish } | LocalTheme | Nullish;
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

export const itemThemeCss = (
  themeSource: ItemThemeProvider,
  defaultTheme?: LocalTheme | Nullish,
  merge?: object,
): React.CSSProperties => {
  const theme = resolveTheme(themeSource, defaultTheme);

  const primary = cssColor("primary", theme?.primary);
  const primaryContainer = cssColor(
    "primary-container",
    getContainerColor(primary["--primary"], primary["--on-primary"]),
  );
  const accent = cssColor("accent", theme?.accent);

  return {
    ...(merge ?? {}),
    ...Object.fromEntries(
      Object.entries({
        ...primary,
        ...primaryContainer,
        ...accent,
        accentColor: theme?.primary,
      }).filter(([_, value]) => !!value),
    ),
  };
};
const cssColor = (name: string, color: string | undefined) => {
  const background = color;
  const foreground = getOnColor(color);

  return {
    [`--${name}`]: background,
    [`--on-${name}`]: foreground,
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
  const themedStyle = itemThemeCss(themeSource, defaultTheme, style);

  if (
    !isPartyLike(themeSource) ||
    (!themeSource?.logo_mask && !themeSource?.logo)
  ) {
    return (
      <div
        style={{
          ...themedStyle,
        }}
        {...addClass(rest, "surface-primary-container")}
      >
        {children}
      </div>
    );
  }

  return (
    <div
      style={{
        ...themedStyle,
      }}
      {...addClass(rest, "relative overflow-hidden surface-primary-container")}
    >
      <MaskedSvg
        src={themeSource.logo_mask ?? themeSource.logo}
        className="absolute inset-0 size-full translate-x-1/2 bg-black/[0.08]"
      />

      {children}
    </div>
  );
};
