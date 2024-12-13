import { ComponentPropsWithoutRef } from "react";
import { addClass, classes } from "@/util/transforms";
import { AppIcon, Icon } from "@/components/icon";
import Link from "next/link";

export const TextButton = (props: ButtonProps) => {
  return (
    <BaseButton
      {...addClass(
        props,
        "rounded font-bold tracking-tight hover:bg-surface-50/15",
      )}
    />
  );
};

export const TintedButton = (props: ButtonProps) => {
  return (
    <BaseButton
      {...addClass(
        props,
        "rounded-lg  px-2 py-1",
        "[background-color:--accent] [color:--on_accent]",
      )}
    />
  );
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

const ButtonContent = (
  props: ButtonContentProps & ComponentPropsWithoutRef<"div">,
) => {
  const { icon, children, ...rest } = addClass(
    props,
    "line-clamp-1 flex items-center gap-1",
  );

  return (
    <div {...rest}>
      <Icon icon={icon} className="fill-current opacity-90" />
      {children}
    </div>
  );
};

const BaseButton = (props: ButtonProps) => {
  const { icon, children, ...rest } = addClass(
    props,
    "inline-block hover:cursor-pointer transition-all",
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
      className={classes("pointer-events-none", props.className)}
      {...(rest as ComponentPropsWithoutRef<"div">)}
    >
      {content}
    </div>
  );
};
