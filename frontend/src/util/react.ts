export const classes = (...classNames: (string | null | undefined)[]) => {
  return classNames.filter(Boolean).join(" ");
};
