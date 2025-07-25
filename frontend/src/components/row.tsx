import React from "react";
import { onlyIf } from "@/components/optional";
import { DivProps } from "@/types/react";
import { AlignItems, JustifyContent } from "@/types/tailwind";
import { addClass } from "@/util/transforms";

interface RowProps {
  overflow?: "scroll" | "wrap" | undefined;
  vertical?: AlignItems;
  horizontal?: JustifyContent;
  padEdge?: boolean;
}
export const Row = (props: DivProps<RowProps>) => {
  const {
    overflow,
    horizontal,
    vertical = "items-center",
    padEdge,
    ...rest
  } = props;
  return (
    <div
      {...addClass(
        rest,
        "row",
        onlyIf(overflow === "wrap", "row-wrap"),
        onlyIf(overflow === "scroll", "row-scroll"),
        onlyIf(padEdge, "*:first:ms-edge *:last:me-edge"),
        horizontal,
        vertical,
      )}
    />
  );
};

export const SeparatedRow = (props: DivProps<RowProps>) => {
  const { overflow = "wrap", ...rest } = props;
  return (
    <Row
      overflow={overflow}
      {...addClass(
        rest,
        "*:not-last:after:content-['·'] *:not-last:after:mx-ch",
      )}
    />
  );
};
