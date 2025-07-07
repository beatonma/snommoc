"use client";

import Link from "next/link";
import { CSSProperties, Children as ReactChildren, ReactNode } from "react";
import Icon, { type AppIcon, isIcon } from "@/components/icon";
import { onlyIf } from "@/components/optional";
import { useTooltip } from "@/components/tooltip";
import { Nullish } from "@/types/common";
import { ClassNameProps, Props } from "@/types/react";
import { addClass, classes } from "@/util/transforms";

interface ButtonIconProps {
  icon?: AppIcon | string;
  iconProps?: {
    className?: string;
    style?: CSSProperties;
  };
}

interface ButtonContentProps {
  tooltip?: string;

  contentClass?: string;

  /* If true, reverse content layout so the icon is on the right side of the button. */
  reverseLayout?: boolean;
}
interface ButtonColors {
  colors?: string;
}

/* Attributes that appear in button override those from Link, and both override the attributes of span. */
type ContainerElementProps = Props<
  "span",
  Props<typeof Link, { href?: string | Nullish } & Props<"button">>
>;
export type ButtonProps = ButtonIconProps &
  ButtonContentProps &
  ButtonColors &
  ContainerElementProps;

/**
 * A button with no padding which shows a larger background on hover.
 */
export const InlineButton = (props: ButtonProps) => {
  const { children, ...rest } = addClass(
    props,
    "relative select-none no-underline! rounded-sm font-bold tracking-tight",
    "hover-extra-background",
    "before:-inset-x-2 before:-inset-y-1",
  );
  return <BaseButton {...rest}>{children}</BaseButton>;
};

/**
 * A typical button with customisable colors.
 */
export const Button = (props: ButtonProps) => {
  const { colors, ...rest } = addClass(
    props,
    "rounded-md px-2 py-1 min-w-[2em] min-h-[2em]",
    "select-none font-bold no-underline!",
  );
  return (
    <BaseButton colors={colors || "hover:not-disabled:bg-hover"} {...rest} />
  );
};

/**
 * A button styled with the current `primary` theme color.
 */
export const TintedButton = (props: ButtonProps) => {
  return (
    <Button
      colors="surface-primary-container hover-surface-primary-container"
      {...props}
    />
  );
};

/**
 * A typical link with automatic formatting and optional icon.
 */
export const InlineLink = (props: ButtonProps) => {
  const { href, ...rest } = addClass(props, "hover:underline");

  return <BaseButton href={href ?? undefined} {...rest} />;
};

const BaseButton = (props: ButtonProps) => {
  const {
    icon,
    iconProps,
    tooltip,
    colors: _colors,
    reverseLayout,
    contentClass,
    children,
    ...rest
  } = addClass(
    props,
    "isolate relative transition-all",
    "inline-flex items-center justify-center",
    "hover:cursor-pointer",
    "disabled:cursor-not-allowed disabled:contrast-40",
    props.colors,
  );

  const tooltipAttrs = useTooltip({ tooltip });

  const content = (
    <>
      <span className="absolute size-full touch-target pointer:hidden" />
      <ButtonContent
        icon={icon}
        iconProps={iconProps}
        reverseLayout={reverseLayout}
        contentClass={contentClass}
      >
        {children}
      </ButtonContent>
    </>
  );

  if (isLink(rest)) {
    return (
      <Link {...rest} {...tooltipAttrs}>
        {content}
      </Link>
    );
  }
  if (isButton(rest)) {
    return (
      <button {...rest} {...tooltipAttrs}>
        {content}
      </button>
    );
  }

  // Strip any `hover:` or `hover-` classes from className. Don't use
  // `pointer-events-none` as that prevents tooltip from working.
  const { className: originalClassName, ...divRest } = addClass(
    rest,
    "cursor-default",
  ) as Props<"span">;
  const noHoverClassName = originalClassName?.replace(
    /(^|\s+)hover[-:]\S+/g,
    "",
  );

  // No usable href or onClick - render as simple div.
  return (
    <span className={noHoverClassName} {...divRest} {...tooltipAttrs}>
      {content}
    </span>
  );
};

const isLink = (obj: any): obj is { href: string } & Props<typeof Link> => {
  return "href" in obj && obj.href;
};
const isButton = (obj: any): obj is Props<"button"> => {
  return (
    ("onClick" in obj && typeof obj.onClick === "function") ||
    ("type" in obj && obj.type === "submit")
  );
};

const ButtonContent = (
  props: ButtonContentProps & ButtonIconProps & { children?: ReactNode },
) => {
  const {
    icon,
    iconProps,
    children,
    contentClass,
    reverseLayout = false,
  } = props;

  if (icon && ReactChildren.count(children) === 0)
    return <ButtonIcon icon={icon} />;

  return (
    <span
      className={classes(
        contentClass,
        "grid items-center space-x-1",
        "grid-cols-[auto_1fr]",
        "grid-rows-1",
        onlyIf(reverseLayout, "[direction:rtl]"),
      )}
    >
      <ButtonIcon icon={icon} iconProps={iconProps} className="col-start-1" />
      <span className="line-clamp-1 break-all overflow-ellipsis leading-none col-start-2">
        {children}
      </span>
    </span>
  );
};

const ButtonIcon = (props: ButtonIconProps & ClassNameProps) => {
  const { icon, iconProps, ...rest } = addClass(
    props,
    props.iconProps?.className || "fill-current/90",
  );

  if (!icon && !iconProps) return null;

  if (icon && isIcon(icon)) {
    return <Icon icon={icon as AppIcon} style={iconProps?.style} {...rest} />;
  }
  return (
    <span>
      <span
        {...addClass(
          rest,
          "inline-flex items-center justify-center w-ch aspect-square",
        )}
        style={iconProps?.style}
      />
    </span>
  );
};
