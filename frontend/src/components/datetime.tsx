import { Nullish } from "@/types/common";
import { DivPropsNoChildren } from "@/types/react";
import { ComponentPropsWithoutRef } from "react";
import { addClass, capitalize } from "@/util/transforms";

type ParseableDate = Date | string | number | Nullish;
const DefaultDateFormat: Intl.DateTimeFormatOptions = {
  year: "numeric",
  month: "long",
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
    dateFormat?: Intl.DateTimeFormatOptions;
    capitalized?: boolean;
  } & DivPropsNoChildren,
) => {
  const {
    start: _start,
    end: _end,
    dateFormat,
    capitalized = true,
    ...rest
  } = addClass(props, "flex gap-x-0.5");
  const start = parseDate(props.start);
  const end = parseDate(props.end);

  if (start && end) {
    return (
      <div {...rest}>
        <Date date={start} dateFormat={dateFormat} />-
        <Date date={end} dateFormat={dateFormat} />
      </div>
    );
  }

  if (start) {
    const prefix = "since";
    return (
      <div {...rest}>
        {`${capitalized ? capitalize(prefix) : prefix}`}{" "}
        <Date date={start} dateFormat={dateFormat} />
      </div>
    );
  }
};

export const Date = (
  props: {
    date: ParseableDate;
    dateFormat?: Intl.DateTimeFormatOptions;
  } & Omit<ComponentPropsWithoutRef<"time">, "dateTime" | "children" | "title">,
) => {
  const { date, dateFormat = DefaultDateFormat, ...rest } = props;
  const parsed = parseDate(date);

  if (parsed == null) return null;

  return (
    <time
      dateTime={parsed.toDateString()}
      title={parsed.toDateString()}
      {...rest}
    >
      {parsed.toLocaleDateString(undefined, dateFormat)}
    </time>
  );
};
