"use client";

import React, { ReactNode, useEffect, useState } from "react";

interface SortBy<T> {
  name: string;
  sort: (a: T, b: T) => number;
}
interface InternalSortBy<T> extends SortBy<T> {
  key: string;
}
type SortOptions<T> = Record<string, SortBy<T>>;

// useSortable input
interface SortableProps<T, O extends SortOptions<T>> {
  data: T[];
  sortOptions: O;
  defaultSort?: keyof O;
  uiElementOptions?: {
    selectClass?: string;
    optionClass?: string;
  };
}

// useSortable output
interface SortedResult<T, S> {
  sortedData: T[] | undefined;

  // An <option> element to be used in calling UI.
  sortBySelectElement: ReactNode;

  // The currently chosen sort option.
  sortedBy: S;
}

export const useSortable = <T, O extends SortOptions<T>>(
  props: SortableProps<T, O>,
): SortedResult<T, keyof O> => {
  const { data, defaultSort, uiElementOptions } = props;
  const [sortedData, setSortedData] = useState<T[]>();

  // Map props.sortOptions (a Record<string, SortBy>) to InternalSortBy[].
  const [sortOptions] = useState<InternalSortBy<T>[]>(() =>
    buildSortOptions(props.sortOptions, defaultSort),
  );

  const [sortBy, setSortBy] = useState<InternalSortBy<T>>(() =>
    chooseSort(sortOptions, defaultSort as string),
  );

  useEffect(() => {
    setSortedData(data.toSorted(sortBy.sort));
  }, [data, sortBy]);

  return {
    sortedBy: sortBy.key,
    sortedData: sortedData,
    sortBySelectElement: (
      <select
        value={sortBy.key}
        className={uiElementOptions?.selectClass}
        onChange={(event) =>
          setSortBy(chooseSort(sortOptions, event.target.value))
        }
      >
        {sortOptions.map(({ key, name }) => {
          return (
            <option
              key={key}
              value={key}
              className={uiElementOptions?.optionClass}
            >
              {name}
            </option>
          );
        })}
      </select>
    ),
  };
};

const buildSortOptions = <T, O extends SortOptions<T>>(
  sortOptions: O,
  defaultSort: keyof O | undefined,
): InternalSortBy<T>[] => {
  const options = {
    ...(defaultSort
      ? {}
      : { _default: { name: "-", sort: () => 0 } as SortBy<T> }),
    ...sortOptions,
  };

  return (Object.entries(options) as [string, SortBy<T>][]).map(
    ([key, value]) => ({
      key: key,
      name: value.name,
      sort: value.sort,
    }),
  );
};

const chooseSort = <T,>(
  sortOptions: InternalSortBy<T>[],
  key?: string | undefined,
): InternalSortBy<T> => {
  if (!key) return sortOptions[0]!;
  return sortOptions.find((it) => it.key === key)!;
};
