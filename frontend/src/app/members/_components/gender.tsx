import { Props } from "@/types/react";

export const Gender = (
  props: Props<"span", { gender: string | null }, "title" | "children">,
) => {
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
};
