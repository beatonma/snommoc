import { int } from "@/components/number";

/**
 * [Single: ZeroOrMany]
 */
const Plurals = {
  MP: ["MP", "MPs"],
  Lord: ["Lord", "Lords"],
  Member: ["Member", "Members"],
  result: ["result", "results"],
  vote: ["vote", "votes"],
};

export const plural = (key: keyof typeof Plurals, count: number) => {
  const index = count === 1 ? 0 : 1;

  return `${int(count)} ${Plurals[key][index]}`;
};
