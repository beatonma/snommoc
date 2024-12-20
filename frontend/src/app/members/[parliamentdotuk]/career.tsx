import { getMemberCareer, MemberCareer } from "@/api";
import ErrorMessage from "@/components/error";
import { Date, DateRange } from "@/components/datetime";
import React, { ComponentPropsWithoutRef, ReactNode } from "react";
import {
  CommitteeLink,
  ConstituencyLink,
  HouseLink,
  OrganisationLink,
  PartyLink,
  PostLink,
} from "@/components/linked-data";
import { SeparatedRow } from "@/components/collection";
import { Nullish } from "@/types/common";
import { Optional } from "@/components/optional";
import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

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

export default async function Career(props: { parliamentdotuk: number }) {
  const { parliamentdotuk } = props;
  const response = await getMemberCareer(parliamentdotuk);
  const career = response.data;
  if (!career) return <ErrorMessage error="Career not available." />;

  return (
    <>
      <h2>Career</h2>

      <Summary
        houses={career.houses}
        parties={career.parties}
        constituencies={career.constituencies}
      />

      <Houses houses={career.houses} />
      <Parties parties={career.parties} />
      <Constituencies constituencies={career.constituencies} />

      <SubjectsOfInterest subjects={career.subjects_of_interest} />

      <Posts posts={career.posts} />
      <Committees committees={career.committees} />
      <Interests interests={career.interests} />
      <Experiences experiences={career.experiences} />
    </>
  );
}

/**
 * Display a reduced UI for sections that don't have much to say.
 */
const Summary = (props: CareerSummary) => {
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

interface SectionProps<T> {
  title: string;
  description?: string;
  data: T | Nullish;
  block: (data: T) => ReactNode;
}

const Section = <T,>(
  props: SectionProps<T> &
    Omit<
      ComponentPropsWithoutRef<"section">,
      keyof SectionProps<T> | "id" | "children"
    >,
) => {
  const { title, description, data, block, ...rest } = props;

  if (!data) return null;
  if (typeof data === "object" && !Object.keys(data).length) return null;

  return (
    <section id={title.toLowerCase().replaceAll(/\s/g, "")} {...rest}>
      <h3>{title}</h3>

      <Optional
        value={description}
        block={(it) => <div className="text-lg">{it}</div>}
      />

      {block(data)}
    </section>
  );
};

interface ListProps<T> {
  title: string;
  description?: string;
  data: T[];
  block: (item: T) => ReactNode;
}
type ListSectionProps<T> = ListProps<T> &
  Omit<
    ComponentPropsWithoutRef<"section">,
    keyof ListProps<T> | "id" | "children"
  >;
const ListSection = <T,>(props: ListSectionProps<T>) => {
  if (!props.data.length) return null;

  const { data, block, ...rest } = props;

  return (
    <Section
      data={data}
      block={(items) =>
        items.map((it, index) => (
          <React.Fragment key={index}>{block(it)}</React.Fragment>
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
  props: ListSectionProps<CareerSummary[T][number]>,
) => {
  if (props.data.length <= 1) return null;

  return <ListSection {...props} />;
};

const Parties = ({ parties }: { parties: CareerParty[] }) => (
  <SummaryListSection
    title="Parties"
    data={parties}
    block={(it) => <PartyItem item={it as CareerParty} />}
  />
);

const Constituencies = ({
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

const Houses = ({ houses }: { houses: CareerHouse[] }) => (
  <SummaryListSection
    title="Houses"
    data={houses}
    block={(it) => <HouseItem item={it as CareerHouse} />}
  />
);

const Posts = ({ posts }: { posts: MemberCareer["posts"] }) => (
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

const Committees = ({
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

const Experiences = ({
  experiences,
}: {
  experiences: MemberCareer["experiences"];
}) => (
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

const SubjectsOfInterest = ({
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

const Interests = ({ interests }: { interests: MemberCareer["interests"] }) => (
  <ListSection
    className="gap-y-4"
    title="Registered Interests"
    data={interests}
    block={(it) => (
      <BlockItem>
        <Date date={it.created} />
        <div>{it.category}</div>
        <div>
          {it.description.map((par, index) => {
            return <p key={index}>{par}</p>;
          })}
        </div>
      </BlockItem>
    )}
  />
);

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
