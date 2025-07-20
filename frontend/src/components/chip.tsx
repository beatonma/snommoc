import { Props } from "@/types/react";
import { addClass } from "@/util/transforms";

export const Chip = (props: Props<"span", { colors?: string }>) => {
  const { colors = "surface-primary", ...rest } = props;
  return <span {...addClass(rest, "chip chip-content", colors)} />;
};
