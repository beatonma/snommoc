import Link from "next/link";
import React, { ReactNode } from "react";
import { onlyIf } from "@/components/optional";
import {
  ItemTheme,
  ItemThemeableProps,
  itemThemeCss,
} from "@/features/themed/item-theme";
import type { DivProps, Props } from "@/types/react";
import { addClass } from "@/util/transforms";

type HeaderCardProps = DivProps<
  { hero?: ReactNode; inlineImage?: ReactNode } & ItemThemeableProps
>;
export const HeaderCard = (props: HeaderCardProps) => {
  const { inlineImage, hero, children, themeSource, ...rest } = props;

  return (
    <ItemTheme
      themeSource={themeSource}
      {...addClass(
        rest,
        "@container grid card w-full readable",
        "grid-cols-[auto_1fr] grid-rows-[auto-auto] themed-surface",
        "[--x-spacing:--spacing(2)] sm:[--x-spacing:--spacing(4)]",
      )}
    >
      {onlyIf(hero, <div className="col-span-full">{hero}</div>)}

      <div
        className="grid grid-rows-subgrid grid-cols-subgrid
      space-x-(--x-spacing) px-(--x-spacing) py-4 col-span-full"
      >
        {onlyIf(inlineImage, <>{inlineImage}</>)}
        <div className="col-start-2">{children}</div>
      </div>
    </ItemTheme>
  );
};

type ListItemCardProps = Props<
  typeof Link,
  {
    hero?: ReactNode;
    inlineImage?: ReactNode;
    label?: ReactNode;
    border?: boolean;
  } & ItemThemeableProps
>;
export const ListItemCard = (props: ListItemCardProps) => {
  const {
    inlineImage,
    hero,
    children,
    themeSource,
    defaultTheme,
    border = false,
    label,
    style,
    ...rest
  } = props;

  const themedStyle = itemThemeCss(themeSource, defaultTheme, style);

  return (
    <Link
      style={themedStyle}
      {...addClass(
        rest,
        "@container card grid grid-cols-[auto_1fr] grid-rows-[auto-auto] ",
        "themed-surface-clickable w-listitem-card [--x-spacing:--spacing(2)] sm:[--x-spacing:--spacing(4)]",
      )}
    >
      {onlyIf(hero, <div className="col-span-full">{hero}</div>)}

      <div
        className="grid grid-rows-subgrid grid-cols-subgrid
      space-x-(--x-spacing) px-(--x-spacing) py-4 col-span-full"
      >
        {onlyIf(
          inlineImage,
          <div
            className="bg-[color-mix(in_srgb,var(--primary),var(--background))]
            border-primary border-1 aspect-square size-listitem-card-image shrink-0
            rounded-md overflow-hidden *:w-full empty:hidden @max-2xs:hidden"
          >
            {inlineImage}
          </div>,
        )}

        {onlyIf(
          border && !inlineImage,
          <div className="bg-primary h-full w-[calc(var(--x-spacing)/2)]" />,
        )}

        <div className="col-start-2">
          {onlyIf(
            label,
            <div className="chip chip-content surface-primary-container float-right w-fit text-xs">
              {label}
            </div>,
          )}
          {children}
        </div>
      </div>
    </Link>
  );
};
