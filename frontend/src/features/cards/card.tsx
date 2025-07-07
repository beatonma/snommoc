import Link from "next/link";
import React, { ReactNode } from "react";
import { Optional, onlyIf } from "@/components/optional";
import { Row } from "@/components/row";
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
        "@container grid card w-full readable grid-cols-[auto_1fr] grid-rows-[auto-auto] themed-surface",
        "[--x-spacing:--spacing(2)] sm:[--x-spacing:--spacing(4)]",
      )}
    >
      <Optional
        value={hero}
        block={(it) => <div className="col-span-full">{it}</div>}
      />

      <div className="grid grid-rows-subgrid grid-cols-subgrid space-x-(--x-spacing) px-(--x-spacing) py-4 col-span-full">
        <Optional value={inlineImage} block={(it) => <>{it}</>} />
        <div className="col-start-2">{children}</div>
      </div>
    </ItemTheme>
  );
};

type ListItemCardProps = Props<
  typeof Link,
  { image?: ReactNode; label?: ReactNode } & ItemThemeableProps
>;
export const ListItemCard = (props: ListItemCardProps) => {
  const { image, children, themeSource, defaultTheme, label, style, ...rest } =
    addClass(
      props,
      "@container max-w-listitem-card card themed-surface-clickable block",
      onlyIf(!props.image, "rounded-s-xs"),
    );

  const themedStyle = itemThemeCss(themeSource, defaultTheme, style);

  return (
    <Link style={themedStyle} {...rest}>
      <Row className="size-full" vertical="items-start">
        {image ? (
          <div className="bg-[color-mix(in_srgb,var(--primary),var(--background))] border-primary border-1 m-2 aspect-square size-20 shrink-0 rounded-md overflow-hidden *:w-full empty:hidden @max-2xs:hidden">
            {image}
          </div>
        ) : (
          <div className="bg-primary h-full w-2 me-2" />
        )}

        <div className="w-full p-2 text-sm [&>h2]:text-xl [&>h2]:font-semibold">
          <div className="chip chip-content surface-primary-container float-right w-fit text-xs empty:hidden">
            {label}
          </div>

          {children}
        </div>
      </Row>
    </Link>
  );
};
