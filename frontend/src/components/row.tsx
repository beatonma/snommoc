import React from "react";
import { onlyIf } from "@/components/optional";
import { DivProps } from "@/types/react";
import { AlignItems, JustifyContent } from "@/types/tailwind";
import { addClass } from "@/util/transforms";

interface RowProps {
  overflow?: "scroll" | "wrap" | undefined;
  vertical?: AlignItems;
  horizontal?: JustifyContent;
}
export const Row = (props: DivProps<RowProps>) => {
  const { overflow, horizontal, vertical = "items-center", ...rest } = props;
  return (
    <div
      {...addClass(
        rest,
        "row",
        onlyIf(overflow === "wrap", "row-wrap"),
        onlyIf(overflow === "scroll", "row-scroll"),
        horizontal,
        vertical,
      )}
    />
  );
};

export const SeparatedRow = (props: DivProps) => (
  <div
    {...addClass(
      props,
      `[&>*:not(:last-child)]:after:content-['·'] [&>*:not(:last-child)]:after:mx-1 flex flex-wrap`,
    )}
  />
);
