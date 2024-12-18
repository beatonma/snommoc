import React, {
  ComponentPropsWithoutRef,
  createElement,
  ElementType,
  ReactNode,
} from "react";

type OptionalProps<T> = {
  value: T | null | undefined;
  condition?: (value: T) => boolean;
  block?: (value: T) => ReactNode;
};

type ElementProps<E extends ElementType> = Omit<
  ComponentPropsWithoutRef<E>,
  "children" | keyof OptionalProps<any>
>;

const OptionalElement = <E extends ElementType, T>(
  props: { element: E | null } & ElementProps<E> & OptionalProps<T>,
) => {
  const { element, value, condition, block, ...rest } = props;

  if (value == null) return null;
  if (condition && !condition(value)) return null;
  if (!condition && Array.isArray(value) && value.length === 0) return null;

  const content = (block ?? ((obj) => `${obj}`))(value);
  if (element) {
    return createElement(element, rest, content);
  }
  return <>{content}</>;
};

export const OptionalDiv = <T,>(
  props: OptionalProps<T> & ElementProps<"div">,
) => <OptionalElement element="div" {...props} />;

export const OptionalSpan = <T,>(
  props: OptionalProps<T> & ElementProps<"span">,
) => <OptionalElement element="span" {...props} />;

export const Optional = <T,>(props: OptionalProps<T>) => (
  <OptionalElement element={null} {...props} />
);
