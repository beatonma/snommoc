import { Nullish } from "@/types/common";
import { DivPropsNoChildren, Props } from "@/types/react";
import { addClass, capitalize } from "@/util/transforms";

type ParseableDate = Date | string | number | Nullish;

const DateFormat = {
  Short: {
    year: "numeric",
    month: "long",
  },
  FullDate: {
    day: "numeric",
    year: "numeric",
    month: "long",
  },
} satisfies Record<string, Intl.DateTimeFormatOptions>;
type DateFormat = keyof typeof DateFormat;

export const parseDate = (dt: ParseableDate): Date | null => {
  if (!dt) return null;
  if (dt instanceof globalThis.Date) return dt;

  const result = new globalThis.Date(dt);

  return isNaN(result.valueOf()) ? null : result;
};

export const formatDate = (
  dt: ParseableDate,
  dateFormat: Intl.DateTimeFormatOptions | DateFormat = DateFormat.FullDate,
): string | null => {
  const parsed = parseDate(dt);
  if (!parsed) return null;

  if (typeof dateFormat === "string") {
    dateFormat = DateFormat[dateFormat];
  }

  return parsed.toLocaleDateString(undefined, dateFormat);
};

/**
 * Displays nothing if either date fails to be interpreted as a valid Date.
 */
export const DateRange = (
  props: DivPropsNoChildren<{
    start: ParseableDate;
    end: ParseableDate;
    dateFormat?: Intl.DateTimeFormatOptions | DateFormat;
    capitalized?: boolean;
  }>,
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
      <span {...rest}>
        <Date date={start} dateFormat={dateFormat} />-
        <Date date={end} dateFormat={dateFormat} />
      </span>
    );
  }

  if (start) {
    const prefix = "since";
    return (
      <span {...rest}>
        {`${capitalized ? capitalize(prefix) : prefix}`}{" "}
        <Date date={start} dateFormat={dateFormat} />
      </span>
    );
  }
};

export const Date = (
  props: Props<
    "time",
    {
      date: ParseableDate;
      dateFormat?: Intl.DateTimeFormatOptions | DateFormat;
    },
    "dateTime" | "children" | "title"
  >,
) => {
  const { date, dateFormat = DateFormat.FullDate, ...rest } = props;
  const parsed = parseDate(date);

  if (parsed == null) return null;

  return (
    <time
      dateTime={parsed.toDateString()}
      title={parsed.toDateString()}
      {...rest}
    >
      {formatDate(parsed, dateFormat)}
    </time>
  );
};
