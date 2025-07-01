"use client";

import Link from "next/link";
import { Children as ReactChildren, ReactNode } from "react";
import Icon, { type AppIcon } from "@/components/icon";
import { useTooltip } from "@/components/tooltip";
import { Nullish } from "@/types/common";
import { ClassNameProps, Props, PropsExcept } from "@/types/react";
import { addClass, classes } from "@/util/transforms";

interface ButtonContentProps {
  icon?: AppIcon | ReactNode;
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
export type ButtonProps = ButtonContentProps &
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
  return <Button colors="surface-primary hover-surface-primary" {...props} />;
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
  props: ButtonContentProps & { children?: ReactNode },
) => {
  const { icon, children, contentClass, reverseLayout = false } = props;

  if (icon && ReactChildren.count(children) === 0)
    return <ButtonIcon icon={icon} />;

  const commonWrapperClassName = classes(contentClass, "grid items-center");
  const commonContentClassName = "line-clamp-1 break-all overflow-ellipsis";

  if (reverseLayout) {
    // Put the icon to the right side of the button
    return (
      <span className={classes(commonWrapperClassName, "grid-cols-[1fr_auto]")}>
        <span className={commonContentClassName}>{children}</span>
        <ButtonIcon icon={icon} className="ms-1" />
      </span>
    );
  }

  // Icon on the left side of the button by default.
  return (
    <span className={classes(commonWrapperClassName, "grid-cols-[auto_1fr]")}>
      <ButtonIcon icon={icon} className="me-1" />
      <span className={classes("col-start-2", commonContentClassName)}>
        {children}
      </span>
    </span>
  );
};

const ButtonIcon = (props: ButtonContentProps & ClassNameProps) => {
  const { icon, ...rest } = addClass(props, "fill-current/90");

  if (!icon) return null;

  if (typeof icon === "string") {
    return <Icon icon={icon as AppIcon} {...rest} />;
  }

  return (
    <span
      {...addClass(
        rest,
        "inline-flex items-center justify-center text-sm size-em leading-none",
      )}
    >
      {icon}
    </span>
  );
};
