import {
  ComponentPropsWithoutRef,
  createElement,
  ElementType,
  ReactNode,
} from "react";

type ElementProps<E extends ElementType> = Omit<
  ComponentPropsWithoutRef<E>,
  "children"
>;

interface OptionalProps<T> {
  condition: T | null | undefined;
  block?: ((obj: T) => ReactNode) | undefined;
}

export const Optional = <E extends ElementType, T>(
  props: { element: E } & ElementProps<E> & OptionalProps<T>,
) => {
  const { element, condition, block, ...rest } = props;
  if (condition) {
    const func: (obj: T) => ReactNode = block ?? ((obj) => `${obj}`);
    return createElement(element, rest, func(condition));
  }
};

export const OptionalDiv = <T,>(
  props: OptionalProps<T> & ElementProps<"div">,
) => {
  return <Optional element="div" {...props} />;
};
