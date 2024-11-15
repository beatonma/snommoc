import { ComponentPropsWithoutRef, ReactNode } from "react";
import { classes } from "@/util/react";
import { AppIcon, Icon } from "@/components/icon";
import Link from "next/link";

export const TextButton = (props: ButtonProps) => {
  const { className, ...rest } = props;

  return (
    <BaseButton
      className={classes(
        className,
        "rounded font-bold tracking-tight hover:bg-surface-50/15",
      )}
      {...rest}
    />
  );
};

export const TintedButton = (props: ButtonProps) => {
  const { className, ...rest } = props;

  return (
    <BaseButton
      className={classes(
        className,
        "rounded-lg bg-primary-700 px-2 py-1 text-primary-50 hover:bg-primary-800",
      )}
      {...rest}
    />
  );
};

interface ButtonContentProps {
  icon?: AppIcon;
}
type ButtonProps = ButtonContentProps &
  (
    | ComponentPropsWithoutRef<"button">
    | Omit<ComponentPropsWithoutRef<"a">, "onClick">
    | Omit<ComponentPropsWithoutRef<"div">, "onClick">
  );

const ButtonContent = (
  props: ButtonContentProps & ComponentPropsWithoutRef<"div">,
) => {
  const { icon, className, children, ...rest } = props;
  return (
    <div
      className={classes(className, "line-clamp-1 flex items-center gap-1")}
      {...rest}
    >
      <Icon icon={icon} className="fill-current opacity-90" />
      {children}
    </div>
  );
};

const BaseButton = (props: ButtonProps) => {
  const { icon, children, className, ...rest } = props;

  const cls = classes(
    className,
    "inline-block hover:cursor-pointer transition-all",
  );
  const content = <ButtonContent icon={icon}>{children}</ButtonContent>;

  if ("href" in rest && rest.href) {
    return (
      <Link
        href={rest.href}
        className={cls}
        {...(rest as ComponentPropsWithoutRef<"a">)}
      >
        {content}
      </Link>
    );
  }
  if ("onClick" in rest && typeof rest.onClick === "function") {
    return (
      <button className={cls} {...rest}>
        {content}
      </button>
    );
  }

  // No usable href or onClick - render as simple div.
  return (
    <div
      // className="pointer-events-none"
      className={classes("pointer-events-none", cls)}
      {...(rest as ComponentPropsWithoutRef<"div">)}
    >
      {content}
    </div>
  );
};
