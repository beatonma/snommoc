import React, { ReactNode, useId } from "react";
import { MemberCareer } from "@/api/schema";
import { DateRange } from "@/components/datetime";
import { LoadingSpinner } from "@/components/loading";
import { onlyIf } from "@/components/optional";
import { Row } from "@/components/row";
import { Nullish } from "@/types/common";
import { DivProps, Props } from "@/types/react";
import { addClass } from "@/util/transforms";

export const SecondaryStyle = "text-reduced text-sm";

interface SectionHeaderProps {
  toolbar?: ReactNode;
}
interface BlockProps<T> extends SectionHeaderProps {
  data: T | Nullish;
  block: (data: T) => ReactNode;
}
interface ListSectionProps<T> extends SectionHeaderProps {
  data: T[] | Nullish;
  block: (item: T, index: number, lst: T[]) => ReactNode;
}
type SectionProps<T extends object> = Props<"section", T, "id" | "children">;

export const Section = <T,>(props: SectionProps<BlockProps<T>>) => {
  const { data, block, ...rest } = props;

  if (!data) return null;
  if (typeof data === "object" && !Object.keys(data).length) return null;

  return <SectionLayout {...rest}>{block(data)}</SectionLayout>;
};

export const SectionLayout = (props: Props<"section", SectionHeaderProps>) => {
  const { title, toolbar, children, ...rest } = props;
  const id = useId();

  return (
    <section id={id} {...rest}>
      {onlyIf(
        toolbar,
        <Row
          overflow="wrap"
          className="gap-x-8 border-1 border-primary/50 px-4 py-2 rounded-sm w-fit surface-primary-container"
        >
          {toolbar}
        </Row>,
      )}

      {children}
    </section>
  );
};

export const ListSection = <T,>(props: SectionProps<ListSectionProps<T>>) => {
  if (props.data == null) return <LoadingSpinner />;
  if (!props.data.length) return null;

  const { data, block, ...rest } = props;

  return (
    <Section
      data={data}
      block={(items) =>
        items.map((it, index, lst) => (
          <React.Fragment key={index}>{block(it, index, lst)}</React.Fragment>
        ))
      }
      {...rest}
    />
  );
};

/**
 * Career components that often only have a single data entry.
 *
 * If that is the case, these should be displayed in <Summary />.
 * Otherwise they should be rendered as full sections using <SummaryListSection />.
 * */
export type CareerSummary = Pick<
  MemberCareer,
  "parties" | "constituencies" | "houses"
>;

export type ListSubheader<T, S extends string> = Record<
  S,
  {
    subheader: (obj: T) => ReactNode;

    // The subheader will be displayed only if consecutive items return
    // different values from this function.
    compare: (obj: T | Nullish) => unknown;
  }
>;
export const ListSubheader = <T,>(props: {
  previous: T;
  current: T;
  compare: (obj: T) => unknown;
  subheader: (item: NonNullable<T>) => ReactNode;
}) => {
  const { previous, current, compare } = props;

  if (compare(previous) === compare(current)) return null;

  return props.subheader(current!);
};

type DateRangeItemProps = DivProps<{
  start: string | Nullish;
  end: string | Nullish;
  capitalized?: boolean;
}>;
export const DateRangeItem = (props: DateRangeItemProps) => {
  const { children, start, end, capitalized = true, ...rest } = props;
  return (
    <span {...rest}>
      {children}
      <DateRange
        className={SecondaryStyle}
        start={start}
        end={end}
        capitalized={capitalized}
      />
    </span>
  );
};
export const InlineDateRangeItem = (props: DateRangeItemProps) => (
  <DateRangeItem
    capitalized={false}
    {...addClass(props, "row-wrap items-baseline gap-x-1")}
  />
);
