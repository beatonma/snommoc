import Link from "next/link";
import React from "react";
import Icon, { type AppIcon } from "@/components/icon";
import { ChildrenProps } from "@/types/common";
import { Props } from "@/types/react";
import { addClass } from "@/util/transforms";

export const TextButton = (props: ButtonProps) => {
  return (
    <BaseButton
      {...addClass(props, "rounded-sm font-bold tracking-tight hover:bg-hover")}
    />
  );
};

export const TintedButton = (props: ButtonProps) => {
  const { style, ...rest } = addClass(
    props,
    "rounded-md px-2 py-1 min-w-[2em] min-h-[2em]",
    "bg-surface text-on_surface",
    "hover:bg-tint_surface_current",
  );

  const themedStyle = {
    ...style,
    "--surface": "var(--accent)",
    "--on_surface": "var(--on_accent)",
  };

  return <BaseButton style={themedStyle} {...rest} />;
};

interface ButtonContentProps {
  icon?: AppIcon;
}
export type ButtonLinkProps = Props<
  "a",
  ButtonContentProps & {
    href: string | null | undefined;
  },
  "onClick"
>;
type ButtonDivProps = Props<"a", ButtonContentProps, "onClick">;
export type ButtonProps =
  | Props<"button", ButtonContentProps>
  | ButtonDivProps
  | ButtonLinkProps;

const isLink = (obj: any): obj is Props<"a"> & { href: string } =>
  "href" in obj && obj.href;
const isButton = (obj: any): obj is Props<"button"> =>
  ("onClick" in obj && typeof obj.onClick === "function") ||
  ("type" in obj && obj.type === "submit");

const ButtonContent = (props: ButtonContentProps & ChildrenProps) => {
  const { icon, children } = props;

  if (icon && React.Children.count(children) === 0)
    return <ButtonIcon icon={icon} />;

  return (
    <div className="flex items-center gap-1">
      <ButtonIcon icon={icon} />
      {children}
    </div>
  );
};

const ButtonIcon = (props: ButtonContentProps) => (
  <Icon className="fill-current/90" {...props} />
);

const BaseButton = (props: ButtonProps) => {
  const { icon, children, ..._rest } = addClass(
    props,
    "inline-flex items-center justify-center hover:cursor-pointer transition-all touch-target select-none",
  );

  const isIconOnly = icon && React.Children.count(children) === 0;
  const content = isIconOnly ? (
    <ButtonIcon icon={icon} />
  ) : (
    <ButtonContent icon={icon}>{children}</ButtonContent>
  );

  const rest = isIconOnly ? addClass(_rest, "aspect-square") : _rest;

  if (isLink(rest)) {
    return <Link {...rest}>{content}</Link>;
  }
  if (isButton(rest)) {
    return <button {...rest}>{content}</button>;
  }

  // No usable href or onClick - render as simple div.
  return (
    <div {...(addClass(rest, "pointer-events-none") as Props<"div">)}>
      {content}
    </div>
  );
};
