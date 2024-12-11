import { MaybeString } from "@/types/common";

export const classes = (...classNames: (MaybeString | null)[]) => {
  return classNames.filter(Boolean).join(" ");
};

interface ClassNameProps {
  className?: MaybeString;
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
  value: MaybeString | null,
  transform: (value: string) => string,
): string | null => (value ? transform(value) : null);

export const capitalize = (value: MaybeString | null): string | null =>
  value ? value.slice(0, 1).toUpperCase() + value.slice(1) : null;
