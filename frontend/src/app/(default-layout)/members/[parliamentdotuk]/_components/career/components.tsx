import React, { ReactNode, useId } from "react";
import { MemberCareer } from "@/api/schema";
import { DateRange } from "@/components/datetime";
import { LoadingSpinner } from "@/components/loading";
import { onlyIf } from "@/components/optional";
import { Row } from "@/components/row";
import { Nullish } from "@/types/common";
import { DivProps, Props } from "@/types/react";

export const SecondaryStyle = "text-reduced text-sm";

interface SectionHeaderProps {
  title: string | undefined;
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

export const SectionLayout = (
  props: Props<"section", { title: string | undefined; toolbar?: ReactNode }>,
) => {
  const { title, toolbar, children, ...rest } = props;
  const id = useId();
  const titleHeader = onlyIf(
    title,
    <h3 className="text-lg text-reduced">{title}</h3>,
  );

  return (
    <section id={id} {...rest}>
      {toolbar ? (
        <Row overflow="wrap" horizontal="justify-between">
          {titleHeader}
          <Row
            overflow="wrap"
            vertical="items-center"
            className="gap-x-8 *:flex *:flex-row *:items-center *:gap-x-2"
          >
            {toolbar}
          </Row>
        </Row>
      ) : (
        titleHeader
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
  <DateRangeItem capitalized={false} {...props} />
);

// {/*{...addClass(props, "flex items-baseline gap-1")}*/}
