import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

export default function Row(props: DivProps) {
  return <div {...addClass(props, "row")} />;
}
