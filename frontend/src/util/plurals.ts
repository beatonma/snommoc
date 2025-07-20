import { int } from "@/components/number";

/**
 * [Single: ZeroOrMany]
 */
type PluralDefinition = [string, string];

const Plurals = {
  MP: ["MP", "MPs"],
  Lord: ["Lord", "Lords"],
  Member: ["Member", "Members"],
  result: ["result", "results"],
  vote: ["vote", "votes"],
  link: ["link", "links"],
} satisfies Record<string, PluralDefinition>;

export const plural = (
  key: keyof typeof Plurals | PluralDefinition,
  count: number,
  format?: (pluralized: string) => string,
) => {
  const index = count === 1 ? 0 : 1;
  const word = (typeof key === "string" ? Plurals[key] : key)[index];

  if (format) {
    return format(word);
  }

  return `${int(count)} ${word}`;
};
