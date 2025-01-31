import { ComponentPropsWithoutRef } from "react";
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

const ButtonContent = (props: ButtonContentProps & ChildrenProps) => {
  const { icon, children } = props;

  return (
    <div className="flex items-center gap-1">
      <Icon icon={icon} className="fill-current opacity-90" />
      {children}
    </div>
  );
};

const BaseButton = (props: ButtonProps) => {
  const { icon, children, ...rest } = addClass(
    props,
    "inline-block align-top hover:cursor-pointer transition-all",
  );

  const content = <ButtonContent icon={icon}>{children}</ButtonContent>;

  if ("href" in rest && rest.href) {
    return (
      <Link href={rest.href} {...(rest as ComponentPropsWithoutRef<"a">)}>
        {content}
      </Link>
    );
  }
  if (rest.type || ("onClick" in rest && typeof rest.onClick === "function")) {
    return (
      <button {...(rest as ComponentPropsWithoutRef<"button">)}>
        {content}
      </button>
    );
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
