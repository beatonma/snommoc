import { ComponentPropsWithoutRef } from "react";
import { classes } from "@/util/react";

export const DetailPage = ({
  className,
  ...rest
}: ComponentPropsWithoutRef<"main">) => {
  return <main className={classes(className, "flex flex-col")} {...rest} />;
};
