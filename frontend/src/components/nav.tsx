import { ComponentPropsWithoutRef } from "react";
import { classes } from "@/util/react";

export const Nav = (props: ComponentPropsWithoutRef<"nav">) => {
  const { className, ...rest } = props;
  return (
    <nav
      className={classes(className, "flex gap-1 text-sm [&>a]:p-1")}
      {...rest}
    />
  );
};
