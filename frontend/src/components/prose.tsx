import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

export const Prose = (props: DivProps) => (
  <div {...addClass(props, "prose readable")} />
);
