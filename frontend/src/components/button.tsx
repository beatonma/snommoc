import React, { ComponentPropsWithoutRef } from "react";
import { addClass } from "@/util/transforms";
import { AppIcon, Icon } from "@/components/icon";
import Link from "next/link";
import { ChildrenProps } from "@/types/common";

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
    "rounded-md px-2 py-1",
    "bg-surface text-on_surface",
    "hover:bg-surface-hover",
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
export type ButtonLinkProps = {
  href: string | null | undefined;
} & ButtonContentProps &
  Omit<ComponentPropsWithoutRef<"a">, "onClick" | "href">;
type ButtonDivProps = ButtonContentProps &
  Omit<ComponentPropsWithoutRef<"a">, "onClick">;
export type ButtonProps =
  | (ButtonContentProps & ComponentPropsWithoutRef<"button">)
  | ButtonDivProps
  | ButtonLinkProps;

const isLink = (
  obj: any,
): obj is ComponentPropsWithoutRef<"a"> & { href: string } => {
  return "href" in obj && obj.href;
};
const isButton = (obj: any): obj is ComponentPropsWithoutRef<"button"> => {
  return "onClick" in obj && typeof obj.onClick === "function";
};

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
    "inline-flex items-center hover:cursor-pointer transition-all",
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
    <div
      {...(addClass(
        rest,
        "pointer-events-none",
      ) as ComponentPropsWithoutRef<"div">)}
    >
      {content}
    </div>
  );
};
