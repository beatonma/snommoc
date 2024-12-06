import { ComponentPropsWithoutRef } from "react";
import { classes } from "@/util/transforms";

interface ElementTheme {
  backgroundColor: string | undefined;
  color: string | undefined;
}
export interface ThemeProps {
  theme?: ElementTheme | undefined;
}
export const ThemedDiv = (
  props: ThemeProps & ComponentPropsWithoutRef<"div">,
) => {
  const { theme, className, ...rest } = props;

  if (theme?.color && theme?.backgroundColor) {
    const style = {
      backgroundColor: theme.backgroundColor,
      color: theme.color,
    };

    return <div style={style} className={className} {...rest} />;
  }

  return (
    <div
      className={classes(
        className,
        "bg-default_party-700 text-default_party-50",
      )}
      {...rest}
    />
  );
};
