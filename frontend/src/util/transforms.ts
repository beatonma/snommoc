export const classes = (...classNames: (string | null | undefined)[]) => {
  return classNames.filter(Boolean).join(" ");
};

interface ClassNameProps {
  className?: string | undefined;
}

/**
 * Returns a copy of props with extraClasses appended to its className attribute.
 */
export const addClass = <T extends ClassNameProps>(
  props: T,
  ...extraClasses: string[]
) => {
  return {
    ...props,
    className: classes(props.className, extraClasses.join(" ")),
  };
};

export const transformString = (
  value: string | undefined | null,
  transform: (value: string) => string,
): string | null => (value ? transform(value) : null);
