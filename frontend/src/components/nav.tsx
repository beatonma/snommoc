import { ComponentPropsWithoutRef } from "react";
import { classes } from "@/util/transforms";

export const Nav = (props: ComponentPropsWithoutRef<"nav">) => {
  const { className, ...rest } = props;
  return (
    <nav
      className={classes(className, "flex flex-wrap gap-1 text-sm [&>a]:p-1")}
      {...rest}
    />
  );
};
