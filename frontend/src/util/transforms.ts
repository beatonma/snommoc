import { Nullish } from "@/types/common";
import { ClassNameProps } from "@/types/react";

export const classes = (...classNames: (string | Nullish)[]) => {
  return classNames.filter(Boolean).join(" ");
};

/**
 * Returns a copy of props with extraClasses appended to its className attribute.
 */
export const addClass = <T extends ClassNameProps>(
  props: T,
  ...extraClasses: (string | Nullish)[]
) => {
  return {
    ...props,
    className: classes(props.className, extraClasses.join(" ")),
  };
};

export const transformString = (
  value: string | Nullish,
  transform: (value: string) => string,
): string | null => (value ? transform(value) : null);

export const capitalize = (value: string | Nullish): string | null =>
  value ? value.slice(0, 1).toUpperCase() + value.slice(1) : null;
