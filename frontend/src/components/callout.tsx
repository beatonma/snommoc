import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

export const Callout = (props: DivProps) => {
  const { children, ...rest } = props;
  return (
    <div {...addClass(rest, "surface-accent px-1 py-1")}>
      <div className="border-s-4 border-on-accent p-2">{children}</div>
    </div>
  );
};
