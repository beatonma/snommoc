import { Nullish } from "@/types/common";
import { DivPropsNoChildren, Props } from "@/types/react";
import { addClass, capitalize } from "@/util/transforms";

type ParseableDate = Date | string | number | Nullish;

export namespace DateFormat {
  export const Default: Intl.DateTimeFormatOptions = {
    year: "numeric",
    month: "long",
  };
  export const FullDate: Intl.DateTimeFormatOptions = {
    day: "numeric",
    year: "numeric",
    month: "long",
  };
}

export const parseDate = (dt: ParseableDate): Date | null => {
  if (!dt) return null;
  if (dt instanceof globalThis.Date) return dt;

  const result = new globalThis.Date(dt);

  return isNaN(result.valueOf()) ? null : result;
};

export const formatDate = (
  dt: ParseableDate,
  dateFormat: Intl.DateTimeFormatOptions = DateFormat.Default,
): string | null => {
  const parsed = parseDate(dt);
  if (!parsed) return null;

  return parsed.toLocaleDateString(undefined, dateFormat);
};

/**
 * Displays nothing if either date fails to be interpreted as a valid Date.
 */
export const DateRange = (
  props: DivPropsNoChildren<{
    start: ParseableDate;
    end: ParseableDate;
    dateFormat?: Intl.DateTimeFormatOptions;
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
  props: Props<
    "time",
    {
      date: ParseableDate;
      dateFormat?: Intl.DateTimeFormatOptions;
    },
    "dateTime" | "children" | "title"
  >,
) => {
  const { date, dateFormat = DateFormat.Default, ...rest } = props;
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
