import { ComponentPropsWithoutRef } from "react";

interface ElementTheme {
  backgroundColor: string | undefined;
  color: string | undefined;
}
export interface ThemeProps {
  theme?: ElementTheme | undefined;
}
export const ThemedDiv = (
  props: ThemeProps & Omit<ComponentPropsWithoutRef<"div">, "color">,
) => {
  const { theme, children, ...rest } = props;

  const style = {
    backgroundColor: theme?.backgroundColor ?? "inherit",
    color: theme?.color ?? "inherit",
  };

  return (
    <div style={style} {...rest}>
      {children}
    </div>
  );
};
