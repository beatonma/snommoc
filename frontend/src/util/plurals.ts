/**
 * [Single: ZeroOrMany]
 */
const Plurals = {
  MP: ["MP", "MPs"],
  Lord: ["Lord", "Lords"],
  Member: ["Member", "Members"],
};

export const plural = (key: keyof typeof Plurals, count: number) => {
  const index = count === 1 ? 0 : 1;

  return `${count} ${Plurals[key][index]}`;
};
