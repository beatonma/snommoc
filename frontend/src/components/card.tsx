import { ComponentProps } from "react";
import { classes } from "@/util/react";

export const Card = (props: ComponentProps<"div">) => {
  const { className, ...rest } = props;
  return (
    <div
      className={classes(
        className,
        "bg-surface-50 text-surface-900 dark:bg-surface-900 dark:text-surface-50",
      )}
      {...rest}
    />
  );
};

export default Card;
