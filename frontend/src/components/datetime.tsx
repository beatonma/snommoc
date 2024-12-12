import { Nullish } from "@/types/common";
import { DivPropsNoChildren } from "@/types/react";
import { ComponentPropsWithoutRef, ReactNode } from "react";
import { SeparatedRow } from "@/components/collection";
import { addClass } from "@/util/transforms";

type ParseableDate = Date | string | number | Nullish;
const DateFormat: Intl.DateTimeFormatOptions = {
  year: "numeric",
  month: "long",
  day: "numeric",
};
const parseDate = (dt: ParseableDate): Date | null => {
  if (!dt) return null;
  if (dt instanceof globalThis.Date) return dt;

  const result = new globalThis.Date(dt);

  return isNaN(result.valueOf()) ? null : result;
};

/**
 * Displays nothing if either date fails to be interpreted as a valid Date.
 */
export const DateRange = (
  props: {
    start: ParseableDate;
    end: ParseableDate;
    prefix?: ReactNode;
    connector?: ReactNode;
    suffix?: ReactNode;
  } & DivPropsNoChildren,
) => {
  const {
    start: _start,
    end: _end,
    prefix,
    suffix,
    ...rest
  } = addClass(props, "flex gap-x-1");
  const start = parseDate(props.start);
  const end = parseDate(props.end);

  if (start && end) {
    return (
      <div {...rest}>
        {prefix}
        <SeparatedRow>
          <Date date={start} />
          <Date date={end} />
        </SeparatedRow>
        {suffix}
      </div>
    );
  }
};

export const Date = (
  props: { date: ParseableDate } & Omit<
    ComponentPropsWithoutRef<"time">,
    "dateTime" | "children"
  >,
) => {
  const { date, ...rest } = props;
  const parsed = parseDate(date);

  if (parsed == null) return null;

  return (
    <time dateTime={parsed.toDateString()} {...rest}>
      {parsed.toLocaleDateString(undefined, DateFormat)}
    </time>
  );
};
