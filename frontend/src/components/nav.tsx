import Link from "next/link";
import { ComponentPropsWithoutRef } from "react";
import { classes } from "@/util/react";

export const Nav = (props: ComponentPropsWithoutRef<"nav">) => {
  const { className, ...rest } = props;
  return (
    <nav
      className={classes(
        className,
        "flex gap-1 text-sm [&>a]:p-1 [&>a]:text-accent-900 dark:[&>a]:text-accent-200",
      )}
      {...rest}
    />
  );
};
