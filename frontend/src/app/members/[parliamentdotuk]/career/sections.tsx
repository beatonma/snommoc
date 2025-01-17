"use client";

import React, { ComponentPropsWithoutRef, ReactNode } from "react";
import { Optional } from "@/components/optional";
import { Nullish } from "@/types/common";
import Loading from "@/components/loading";
import { MemberCareer } from "@/api";
import {
  CommitteeLink,
  ConstituencyLink,
  HouseLink,
  OrganisationLink,
  PartyLink,
  PostLink,
} from "@/components/linked-data";
import {
  Date,
  DateFormat,
  DateRange,
  formatDate,
  parseDate,
} from "@/components/datetime";
import { SeparatedRow } from "@/components/collection";
import { useSortable } from "@/components/sortable";
import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";
import { HighlightMoney } from "@/components/highlight";

const SecondaryStyle = "text-reduced text-sm";

/**
 * Career components that often only have a single data entry.
 *
 * If that is the case, these should be displayed in <Summary />.
 * Otherwise they should be rendered as full sections using <SummaryListSection />.
 * */
type CareerSummary = Pick<
  MemberCareer,
  "parties" | "constituencies" | "houses"
>;
type CareerHouse = MemberCareer["houses"][number];
type CareerConstituency = MemberCareer["constituencies"][number];
type CareerParty = MemberCareer["parties"][number];
/**
 * Display a reduced UI for sections that don't have much to say.
 */
export const Summary = (props: CareerSummary) => {
  const { houses, parties, constituencies } = props;

  const SummaryItem = <T,>(props: {
    items: T[];
    block: (item: T) => ReactNode;
  }) => (
    <Optional
      value={props.items[0]}
      condition={() => props.items.length === 1}
      block={props.block}
    />
  );

  return (
    <section>
      <SummaryItem items={parties} block={(it) => <PartyItem item={it} />} />
      <SummaryItem
        items={constituencies}
        block={(it) => <ConstituencyItem prefix="MP for" item={it} />}
      />
      <SummaryItem
        items={houses}
        block={(it) => (
          <HouseItem item={it} longFormat={true} prefix="Member of" />
        )}
      />
    </section>
  );
};

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

const Section = <T,>(props: SectionProps<BlockProps<T>>) => {
  const { title, toolbar, description, data, block, ...rest } = props;

  if (!data) return null;
  if (typeof data === "object" && !Object.keys(data).length) return null;

  const titleHeader = <h3>{title}</h3>;

  return (
    <section id={title.toLowerCase().replaceAll(/\s/g, "")} {...rest}>
      {toolbar ? (
        <div className="flex flex-row justify-between">
          {titleHeader}
          <div className="flex flex-row items-center gap-x-2">{toolbar}</div>
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

const ListSection = <T,>(props: SectionProps<ListSectionProps<T>>) => {
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
 * A ListSection which should only render if there are multiple items in the given
 * data.
 * Empty data should not render at all.
 * Data with a single item will instead be rendered in <Summary />
 */
const SummaryListSection = <T extends keyof CareerSummary>(
  props: SectionProps<ListSectionProps<CareerSummary[T][number]>>,
) => {
  if (props.data == null) return <Loading />;
  if (props.data.length <= 1) return null;

  return <ListSection {...props} />;
};

export const Parties = ({ parties }: { parties: CareerParty[] }) => (
  <SummaryListSection
    title="Parties"
    data={parties}
    block={(it) => <PartyItem item={it as CareerParty} />}
  />
);

export const Constituencies = ({
  constituencies,
}: {
  constituencies: CareerConstituency[];
}) => (
  <SummaryListSection
    title="Constituencies"
    data={constituencies}
    block={(it) => <ConstituencyItem item={it as CareerConstituency} />}
  />
);

export const Houses = ({ houses }: { houses: CareerHouse[] }) => (
  <SummaryListSection
    title="Houses"
    data={houses}
    block={(it) => <HouseItem item={it as CareerHouse} />}
  />
);

export const Posts = ({ posts }: { posts: MemberCareer["posts"] }) => (
  <ListSection
    title="Posts"
    data={posts}
    block={(post) => (
      <BlockItem>
        <PostLink post={post} />
        <DateRange
          className={SecondaryStyle}
          start={post.start}
          end={post.end}
        />
      </BlockItem>
    )}
  />
);

export const Committees = ({
  committees,
}: {
  committees: MemberCareer["committees"];
}) => (
  <ListSection
    title="Committees"
    data={committees}
    block={(it) => (
      <BlockItem>
        <CommitteeLink committee={it} />
        <DateRange className={SecondaryStyle} start={it.start} end={it.end} />
      </BlockItem>
    )}
  />
);

export const Experiences = ({
  experiences,
}: {
  experiences: MemberCareer["experiences"];
}) => {
  return (
    <ListSection
      title="Non-parliamentary experience"
      data={experiences}
      block={(it) => (
        <BlockItem>
          <div>
            <span>{it.title}</span>
            <span> at </span>
            <OrganisationLink organisation={it.organisation} />
          </div>

          <SeparatedRow className={SecondaryStyle}>
            <span>{it.category}</span>
            <DateRange start={it.start} end={it.end} />
          </SeparatedRow>
        </BlockItem>
      )}
    />
  );
};

export const SubjectsOfInterest = ({
  subjects,
}: {
  subjects: MemberCareer["subjects_of_interest"];
}) => (
  <Section
    className="gap-y-4"
    title="Subjects of interest"
    data={subjects}
    block={(data) =>
      Object.entries(data).map(([category, items]) => (
        <div key={category}>
          <div className="text-lg">{category}</div>
          <ul>
            {items.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      ))
    }
  />
);

type Interest = MemberCareer["interests"][number];
export const RegisteredInterests = ({
  interests,
}: {
  interests: MemberCareer["interests"];
}) => {
  const { sortedData, sortBySelectElement, sortedBy } = useSortable({
    data: interests,
    defaultSort: "date",
    sortOptions: {
      category: {
        name: "Category",
        sort: (a, b) => (a.category ?? "").localeCompare(b.category ?? ""),
      },
      date: {
        name: "Recent",
        sort: (a, b) =>
          (parseDate(b.created)?.getTime() ?? 0) -
          (parseDate(a.created)?.getTime() ?? 0),
      },
    },
  });

  const subheader: ListSubheader<Interest, typeof sortedBy> = {
    category: {
      subheader: (obj) => obj.category,
      compare: (obj) => obj?.category,
    },
    date: {
      subheader: (obj) => <Date date={obj.created} />,
      compare: (obj) => formatDate(obj?.created),
    },
  };

  return (
    <ListSection
      className="gap-y-4"
      title="Registered Interests"
      toolbar={<>Sort: {sortBySelectElement}</>}
      data={sortedData}
      block={(it, index, lst) => {
        return (
          <>
            <ListSubheader
              previous={lst[index - 1]}
              current={lst[index]}
              compare={(it) => subheader[sortedBy].compare(it)}
              subheader={(it) => <h4>{subheader[sortedBy].subheader(it)}</h4>}
            />

            <RegisteredInterest interest={it} />
          </>
        );
      }}
    />
  );
};
const RegisteredInterest = (props: { interest: Interest } & DivProps) => {
  const { interest, ...rest } = props;
  return (
    <BlockItem {...rest}>
      <SeparatedRow className="text-sm">
        <Date date={interest.created} dateFormat={DateFormat.FullDate} />
        <div>{interest.category}</div>
      </SeparatedRow>
      <div>
        {interest.description.map((par, index) => {
          return (
            <p key={index}>
              <HighlightMoney text={par} className="font-bold" />
            </p>
          );
        })}
      </div>

      {interest.children.map((child, index) => (
        <RegisteredInterest
          key={index}
          interest={child}
          className="my-2 border-l-2 border-primary pl-2"
        />
      ))}
    </BlockItem>
  );
};

type ListSubheader<T, S extends string> = Record<
  S,
  {
    subheader: (obj: T) => ReactNode;

    // The subheader will be displayed only if consecutive items return
    // different values from this function.
    compare: (obj: T | Nullish) => unknown;
  }
>;
const ListSubheader = <T,>(props: {
  previous: T;
  current: T;
  compare: (obj: T) => unknown;
  subheader: (item: NonNullable<T>) => ReactNode;
}) => {
  const { previous, current, compare } = props;

  if (compare(previous) === compare(current)) return null;

  return props.subheader(current!);
};
const BlockItem = (props: DivProps) => {
  return <div {...props} />;
};
const InlineDateRangeItem = (props: {
  prefix?: ReactNode;
  text: ReactNode;
  start: string | Nullish;
  end: string | Nullish;
}) => {
  const { prefix, text, start, end, ...rest } = props;
  return (
    <div {...addClass(rest, "flex items-baseline gap-1")}>
      {prefix}
      {text}
      <DateRange
        className={SecondaryStyle}
        start={start}
        end={end}
        capitalized={false}
      />
    </div>
  );
};
interface ItemProps<T> {
  item: T;
  prefix?: ReactNode;
}
const PartyItem = (props: ItemProps<CareerParty>) => (
  <InlineDateRangeItem
    prefix={props.prefix}
    text={<PartyLink party={props.item.party} />}
    start={props.item.start}
    end={props.item.end}
  />
);
const ConstituencyItem = (props: ItemProps<CareerConstituency>) => (
  <InlineDateRangeItem
    prefix={props.prefix}
    text={<ConstituencyLink constituency={props.item.constituency} />}
    start={props.item.start}
    end={props.item.end}
  />
);
const HouseItem = (
  props: ItemProps<CareerHouse> & { longFormat?: boolean },
) => (
  <InlineDateRangeItem
    prefix={props.prefix}
    text={
      <HouseLink
        house={props.item.house}
        longFormat={props.longFormat}
        showDot={!props.prefix}
      />
    }
    start={props.item.start}
    end={props.item.end}
  />
);
