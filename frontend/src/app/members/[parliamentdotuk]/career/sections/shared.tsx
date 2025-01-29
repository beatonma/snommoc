import React, { ComponentPropsWithoutRef, ReactNode } from "react";
import { Nullish } from "@/types/common";
import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";
import { DateRange } from "@/components/datetime";
import {
  ConstituencyLink,
  HouseLink,
  PartyLink,
} from "@/components/linked-data";
import { MemberCareer } from "@/api";
import { Optional } from "@/components/optional";
import Loading from "@/components/loading";

export type CareerHouse = MemberCareer["houses"][number];
export type CareerConstituency = MemberCareer["constituencies"][number];
export type CareerParty = MemberCareer["parties"][number];

export const SecondaryStyle = "text-reduced text-sm";

interface SectionHeaderProps {
  title: string;
  toolbar?: ReactNode;
  description?: string;
}
interface BlockProps<T> extends SectionHeaderProps {
  data: T | Nullish;
  block: (data: T) => ReactNode;
}
interface ListSectionProps<T> extends SectionHeaderProps {
  data: T[] | Nullish;
  block: (item: T, index: number, lst: T[]) => ReactNode;
}
type SectionProps<T> = T &
  Omit<ComponentPropsWithoutRef<"section">, keyof T | "id" | "children">;

export const Section = <T,>(props: SectionProps<BlockProps<T>>) => {
  const { title, toolbar, description, data, block, ...rest } = props;

  if (!data) return null;
  if (typeof data === "object" && !Object.keys(data).length) return null;

  const titleHeader = <h3>{title}</h3>;

  return (
    <section id={title.toLowerCase().replaceAll(/\s/g, "")} {...rest}>
      {toolbar ? (
        <div className="flex flex-row justify-between">
          {titleHeader}
          <div className="flex flex-row items-center gap-x-8 [&>*]:flex [&>*]:flex-row [&>*]:items-center [&>*]:gap-x-2">
            {toolbar}
          </div>
        </div>
      ) : (
        titleHeader
      )}

      <Optional
        value={description}
        block={(it) => <div className="text-lg">{it}</div>}
      />

      {block(data)}
    </section>
  );
};

export const ListSection = <T,>(props: SectionProps<ListSectionProps<T>>) => {
  if (props.data == null) return <Loading />;
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

/**
 * A ListSection which should only render if there are multiple items in the given
 * data.
 * Empty data should not render at all.
 * Data with a single item will instead be rendered in <Summary />
 */
export const SummaryListSection = <T extends keyof CareerSummary>(
  props: SectionProps<ListSectionProps<CareerSummary[T][number]>>,
) => {
  if (props.data == null) return <Loading />;
  if (props.data.length <= 1) return null;

  return <ListSection {...props} />;
};

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
export const BlockItem = (props: DivProps) => {
  return <div {...props} />;
};

type DateRangeItemProps = {
  start: string | Nullish;
  end: string | Nullish;
  capitalized?: boolean;
} & DivProps;
export const DateRangeItem = (props: DateRangeItemProps) => {
  const { children, start, end, capitalized = true, ...rest } = props;
  return (
    <BlockItem {...rest}>
      {children}
      <DateRange
        className={SecondaryStyle}
        start={start}
        end={end}
        capitalized={capitalized}
      />
    </BlockItem>
  );
};
export const InlineDateRangeItem = (props: DateRangeItemProps) => (
  <DateRangeItem
    capitalized={false}
    {...addClass(props, "flex items-baseline gap-1")}
  />
);

interface ItemProps<T> {
  item: T;
  prefix?: ReactNode;
}
export const PartyItem = (props: ItemProps<CareerParty>) => (
  <InlineDateRangeItem start={props.item.start} end={props.item.end}>
    {props.prefix}
    <PartyLink party={props.item.party} />
  </InlineDateRangeItem>
);
export const ConstituencyItem = (props: ItemProps<CareerConstituency>) => (
  <InlineDateRangeItem start={props.item.start} end={props.item.end}>
    {props.prefix}
    <ConstituencyLink constituency={props.item.constituency} />
  </InlineDateRangeItem>
);
export const HouseItem = (
  props: ItemProps<CareerHouse> & { longFormat?: boolean },
) => (
  <InlineDateRangeItem start={props.item.start} end={props.item.end}>
    {props.prefix}
    <HouseLink
      house={props.item.house}
      longFormat={props.longFormat}
      showDot={!props.prefix}
    />
  </InlineDateRangeItem>
);
