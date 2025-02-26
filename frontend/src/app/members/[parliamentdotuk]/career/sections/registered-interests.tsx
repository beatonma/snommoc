"use client";
import { MemberCareer } from "@/api";
import { useSortable } from "@/components/sortable";
import { Date, DateFormat, formatDate, parseDate } from "@/components/datetime";
import { DivProps } from "@/types/react";
import React, { useId, useState } from "react";
import { ListSubheader, ListSection, BlockItem, DateRangeItem } from "./shared";
import { HighlightDates } from "@/components/highlight";

const sortByCategory = (a: Interest, b: Interest) =>
  (a.category ?? "").localeCompare(b.category ?? "");
const sortByDateThenCategory = (a: Interest, b: Interest) => {
  const byDate =
    (parseDate(b.created)?.getTime() ?? 0) -
    (parseDate(a.created)?.getTime() ?? 0);
  if (byDate === 0) {
    return sortByCategory(a, b);
  }
  return byDate;
};

type Interest = MemberCareer["interests"][number];
const RegisteredInterests = ({
  interests,
}: {
  interests: MemberCareer["interests"];
}) => {
  const { sortedData, sortBySelectElement, sortedBy } = useSortable({
    data: interests,
    defaultSort: "category",
    sortOptions: {
      category: {
        name: "Category",
        sort: sortByCategory,
      },
      date: {
        name: "Recent",
        sort: sortByDateThenCategory,
      },
    },
    uiElementOptions: {
      label: "Sort:",
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
  const [showDates, setShowDates] = useState(false);
  const showDatesId = useId();

  return (
    <ListSection
      className="gap-y-4"
      title="Registered Interests"
      toolbar={
        <>
          <div>
            <label htmlFor={showDatesId}>Show all dates</label>
            <input
              id={showDatesId}
              type="checkbox"
              checked={showDates}
              onChange={(el) => setShowDates(el.currentTarget.checked)}
            />
          </div>
          <div>{sortBySelectElement}</div>
        </>
      }
      data={sortedData}
      block={(it, index, lst) => {
        return (
          <>
            <ListSubheader
              previous={lst[index - 1]}
              current={lst[index]}
              compare={(it) => subheader[sortedBy].compare(it)}
              subheader={(it) => (
                <h4 className="mt-4">{subheader[sortedBy].subheader(it)}</h4>
              )}
            />

            <RegisteredInterest
              interest={it}
              showDates={showDates}
              showCategory={sortedBy === "date"}
            />
          </>
        );
      }}
    />
  );
};

type RegisteredInterestsProps = {
  interest: Interest;
  showDates: boolean;
  showCategory: boolean;
} & DivProps;

const RegisteredInterest = (props: RegisteredInterestsProps) => {
  const { interest, ...rest } = props;

  if (interest.children.length === 1) {
    // When only one child item, merge that child into the parent before rendering.
    return (
      <RegisteredInterest interest={flattenInterest(interest)} {...rest} />
    );
  }

  if (
    interest.description.table.length === 0 &&
    interest.description.additional_values.length === 1
  ) {
    return <RegisteredInterestDateRangeItem interest={interest} {...rest} />;
  }

  return <RegisteredInterestTable interest={interest} {...rest} />;
};

const RegisteredInterestDateRangeItem = (props: RegisteredInterestsProps) => {
  const { interest, showDates, showCategory, ...rest } = props;
  const description = interest.description;

  return (
    <DateRangeItem
      start={description.start}
      end={description.end}
      className="card card-content surface"
      {...rest}
    >
      {description.additional_values[0]}
    </DateRangeItem>
  );
};

const RegisteredInterestTable = (props: RegisteredInterestsProps) => {
  const { interest, showDates, showCategory, ...rest } = props;

  return (
    <BlockItem {...rest}>
      <table className="w-full table-fixed">
        <colgroup>
          <col className="w-40" />
          <col />
        </colgroup>

        <tbody>
          {interest.description.additional_values.map((row, rowIndex) => (
            <tr key={rowIndex} className="align-top">
              <td colSpan={2}>{row}</td>
            </tr>
          ))}

          {interest.description.table.map((row, rowIndex) => (
            <tr key={rowIndex} className="align-top">
              <th>{row[0]}</th>
              <td>
                <HighlightDates
                  text={row[1].toString()}
                  dateFormat={DateFormat.FullDate}
                />
              </td>
            </tr>
          ))}

          {showDates
            ? interest.description.registration_dates.map(
                ([title, date], rowIndex) => (
                  <tr key={rowIndex} className="align-top">
                    <th>{title}</th>
                    <td>
                      <Date date={date} dateFormat={DateFormat.FullDate} />
                    </td>
                  </tr>
                ),
              )
            : null}
        </tbody>
      </table>

      {interest.children.map((child, index) => (
        <RegisteredInterest
          key={index}
          interest={child}
          showDates={showDates}
          showCategory={false}
          className="border-primary my-2 ml-1 border-l-4 pl-4"
        />
      ))}
    </BlockItem>
  );
};

const flattenInterest = (interest: Interest): Interest => {
  const parentDescription = interest.description;
  const childDescription = interest.children[0]?.description;

  if (!childDescription) {
    throw new Error("Cannot flatten an Interest that has no child Interests.");
  }

  return {
    ...interest,
    description: {
      table: [...parentDescription.table, ...childDescription.table],
      additional_values: [
        ...parentDescription.additional_values,
        ...childDescription.additional_values,
      ],
      registration_dates: childDescription.registration_dates,
      start: childDescription.start ?? parentDescription.start,
      end: childDescription.end ?? parentDescription.end,
    },
    children: [],
  };
};

export default RegisteredInterests;
