import { ComponentPropsWithoutRef } from "react";

export default function Gender(
  props: { gender: string | null } & Omit<
    ComponentPropsWithoutRef<"span">,
    "title" | "children"
  >,
) {
  if (!props.gender) return null;
  const { gender, ...rest } = props;

  const symbols: Record<string, string> = {
    m: "♂",
    f: "♀",
  };

  return (
    <span title={`Gender: ${gender}`} {...rest}>
      {symbols[gender?.toLowerCase()] ?? gender}
    </span>
  );
}
