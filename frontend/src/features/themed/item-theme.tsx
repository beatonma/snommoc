import React from "react";
import type {
  HouseType,
  ItemTheme as LocalTheme,
  Party,
  PartyDetail,
} from "@/api/schema";
import { MaskedSvg } from "@/components/image";
import { getContainerColor, getOnColor } from "@/features/themed/color";
import { NullableValues, Nullish } from "@/types/common";
import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

type Theme = Partial<NullableValues<LocalTheme>>;
type MaybeTheme = Theme | Nullish;
type ItemThemeProvider = { theme: MaybeTheme } | MaybeTheme | HouseType;
export interface ItemThemeableProps {
  themeSource: ItemThemeProvider;
  defaultTheme?: MaybeTheme;
}

const isTheme = (obj: ItemThemeProvider): obj is Theme =>
  obj != null && typeof obj === "object" && "primary" in obj;
const isPartyLike = (obj: ItemThemeProvider): obj is Party | PartyDetail =>
  obj != null && typeof obj === "object" && "logo" in obj;

const resolveTheme = (
  obj: ItemThemeProvider,
  defaultTheme?: MaybeTheme,
): Theme | null => {
  if (!obj) return defaultTheme ?? null;

  if (typeof obj === "string") {
    return getHouseTheme(obj);
  }

  return isTheme(obj) ? obj : (obj.theme ?? null);
};

const getHouseTheme = (house: HouseType): Theme => {
  switch (house) {
    case "Commons":
      return {
        primary: "var(--color-house-commons)",
        on_primary: undefined,
        accent: undefined,
        on_accent: undefined,
      };
    case "Lords":
      return {
        primary: "var(--color-house-lords)",
        on_primary: undefined,
        accent: undefined,
        on_accent: undefined,
      };
  }
};

export const itemThemeCss = (
  themeSource: ItemThemeProvider,
  defaultTheme?: MaybeTheme,
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
const cssColor = (name: string, color: string | Nullish) => {
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
