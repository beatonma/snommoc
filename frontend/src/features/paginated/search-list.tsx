"use client";

import { useSearchParams } from "next/navigation";
import React, { type ReactNode, useId, useMemo, useState } from "react";
import type { PageItemType, Params, Query, SearchablePath } from "@/api/client";
import { TintedButton } from "@/components/button";
import { GridSpan } from "@/components/grid";
import { onlyIf } from "@/components/optional";
import { MaybeString } from "@/types/common";
import { DivPropsNoChildren, State, StateSetter } from "@/types/react";
import { addClass, capitalize } from "@/util/transforms";
import { InfiniteScroll, PaginationItemComponent } from "./infinite-scroll";
import { type Paginated, usePagination } from "./pagination";

const QueryParam = "query";
const DefaultGridClass = "search-results-grid";

export interface SearchFilters {
  singleChoice?: Record<string, SingleChoiceFilter>;
  bool?: Record<string, SearchFilter<boolean>>;
}

interface ListStateProps<P extends SearchablePath> {
  path: P;
  params?: Params<P> | undefined;

  /**
   * User-editable filters applied to search results.
   */
  searchFilters?: SearchFilters;

  /**
   * Filters that are always applied to search results.
   */
  immutableFilters?: Query<P>;
  updateBrowserLocation?: boolean;
}

export interface SearchListState<P extends SearchablePath> {
  pagination: Paginated<PageItemType<P>>;
  queryState: State<string>;
  filtersState: State<SearchFilters>;
  onSearch: () => void;
}
export const useSearchList = <P extends SearchablePath>(
  props: ListStateProps<P>,
): SearchListState<P> => {
  const {
    path,
    params,
    immutableFilters,
    searchFilters,
    updateBrowserLocation,
  } = props;

  const search = useSearchParams();
  const [query, setQuery] = useState<string>(
    search.get(QueryParam) || params?.query?.query || "",
  );
  const [currentQuery, setCurrentQuery] = useState<string>(query);
  const [filters, setFilters, filtersQuery] = useFilters(searchFilters, search);

  const paginationConfigMemo = useMemo(() => {
    return {
      ...params,
      query: {
        ...params?.query,
        ...filtersQuery,
        ...immutableFilters,
        query: currentQuery,
      },
      updateBrowserLocation,
    };
  }, [
    params,
    currentQuery,
    filtersQuery,
    immutableFilters,
    updateBrowserLocation,
  ]);
  const pagination = usePagination(path, paginationConfigMemo);

  return useMemo(
    () => ({
      pagination,
      onSearch: () => setCurrentQuery(query),
      queryState: [query, setQuery],
      filtersState: [filters, setFilters],
    }),
    [pagination, query, filters, setFilters],
  );
};

interface ListPageProps<P extends SearchablePath> {
  header?: ReactNode;
  itemComponent: PaginationItemComponent<PageItemType<P>>;
  gridClassName?: string;
}
export const SearchList = <P extends SearchablePath>(
  props: DivPropsNoChildren<ListPageProps<P> & ListStateProps<P>>,
) => {
  const { path, params, immutableFilters, searchFilters, ...rest } = props;

  const state = useSearchList({
    path,
    params,
    immutableFilters,
    searchFilters,
  });

  return <SearchListLayout state={state} {...rest} />;
};

export const SearchListLayout = <P extends SearchablePath>(
  props: DivPropsNoChildren<ListPageProps<P> & { state: SearchListState<P> }>,
) => {
  const hasHeader = !!props.header;
  const { state, header, itemComponent, gridClassName, ...rest } = addClass(
    props,
    `${props.gridClassName ?? DefaultGridClass} my-2 mb-96 justify-center sm:mx-2`,
  );

  const { pagination, queryState, filtersState, onSearch } = state;
  const [query, setQuery] = queryState;
  const [filters, setFilters] = filtersState;

  return (
    <InfiniteScroll
      {...rest}
      pagination={pagination}
      itemComponent={itemComponent}
      header={
        <GridSpan
          className={`${hasHeader ? "md:justify-between" : "md:justify-center"} flex flex-wrap items-center justify-center`}
        >
          {header}

          <div
            className={`column max-w-[600px] items-center gap-4 p-4 ${onlyIf(hasHeader, "md:items-end")}`}
          >
            <form
              className="row flex-wrap items-center justify-center gap-2"
              onSubmit={(ev) => {
                ev.preventDefault();
                onSearch();
              }}
            >
              <input
                type="search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              <TintedButton type="submit">Search</TintedButton>
            </form>

            <Filters
              filters={filters}
              setFilters={setFilters}
              className="flex gap-6"
            />
          </div>
        </GridSpan>
      }
    />
  );
};

interface SearchFilter<T> {
  label: string;
  value: T;
}
interface FilterValue<T> {
  display: MaybeString;
  value: T;
}

/**
 * Resolve a value which may be either T or FilterValue<T> into a definite FilterValue<T>.
 * @param value
 */
const resolveFilterValue = <T,>(value: T | FilterValue<T>): FilterValue<T> => {
  if (
    value &&
    typeof value === "object" &&
    "display" in value &&
    "value" in value
  ) {
    return value;
  }
  return { display: value ? `${value}` : undefined, value: value };
};

interface SingleChoiceFilter extends SearchFilter<MaybeString> {
  values: (MaybeString | FilterValue<MaybeString>)[];
}
const useFilters = <P extends SearchablePath>(
  init: SearchFilters | undefined,
  initUrlParams: URLSearchParams,
): [SearchFilters, StateSetter<SearchFilters>, Query<P> | undefined] => {
  const [filters, setFilters] = useState<SearchFilters>(() =>
    initFilters(init, initUrlParams),
  );
  const queryFilters = useMemo(() => {
    // Build a flat {key:value} map suitable for use in URLSearchParams.
    const results: Record<string, any> = {};

    Object.values(filters).forEach((filterType: SearchFilter<unknown>) => {
      Object.entries(filterType).forEach(([key, value]) => {
        results[key] = value.value || undefined;
      });
    });
    return results;
  }, [filters]);

  return [filters, setFilters, queryFilters];
};

/**
 * Construct a SearchFilters object which represents the combination of the
 * given values.
 *
 * @param init Default values
 * @param initUrlParams Override defaults from the URL search parameters
 */
const initFilters = (
  init: SearchFilters | undefined,
  initUrlParams: URLSearchParams,
): SearchFilters => {
  const defaults = init ?? {};

  const singleChoice = defaults.singleChoice ?? {};
  for (const [key, value] of Object.entries(singleChoice)) {
    if (initUrlParams.has(key)) {
      const urlValue = initUrlParams.get(key);
      if (!urlValue) continue;

      const possibleValues = value.values;

      for (const v of possibleValues) {
        const _v = resolveFilterValue(v);
        // Only override the default value if the URL value can be resolved
        // to one of the values from SingleChoiceFilter.values.
        if (_v.value?.toLowerCase() === urlValue.toLowerCase()) {
          value.value = _v.value;
        }
      }
    }
  }

  const bool = defaults.bool ?? {};
  for (const [key, value] of Object.entries(bool)) {
    const urlValue = initUrlParams.get(key);
    if (!urlValue) continue;

    if (urlValue.toLowerCase() === "true") {
      value.value = true;
    } else if (urlValue.toLowerCase() === "false") {
      value.value = false;
    }
  }

  return defaults;
};

const Filters = (
  props: DivPropsNoChildren<{
    filters: SearchFilters;
    setFilters: (value: SearchFilters) => void;
  }>,
) => {
  const { filters, setFilters, ...rest } = props;

  return (
    <div {...rest}>
      {Object.entries(filters.singleChoice ?? {}).map(([key, value]) => (
        <SingleChoiceFilter
          key={key}
          label={value.label}
          value={value.value}
          values={value.values}
          onChange={(it) => {
            const newFilters = { ...filters };
            newFilters["singleChoice"]![key]!["value"] = it;
            setFilters(newFilters);
          }}
        />
      ))}

      {Object.entries(filters.bool ?? {}).map(([key, value]) => (
        <BooleanFilter
          key={key}
          label={value.label}
          value={value.value}
          onChange={(it) => {
            const newFilters = { ...filters };
            newFilters["bool"]![key]!["value"] = it;
            setFilters(newFilters);
          }}
        />
      ))}
    </div>
  );
};

interface FilterWidgetProps<T> {
  label: string;
  value: T;
  onChange: (value: T) => void;
}

const SingleChoiceFilter = (
  props: FilterWidgetProps<MaybeString> & SingleChoiceFilter,
) => {
  const { label, values, value, onChange } = props;

  return (
    <FilterLayout
      label={label}
      block={(id) => (
        <select
          id={id}
          value={value}
          onChange={(it) => onChange(it.target.value)}
        >
          {values.map((opt) => {
            const resolved = resolveFilterValue(opt);

            return (
              <option
                key={resolved?.value ?? null}
                value={resolved?.value ?? ""}
              >
                {capitalize(resolved?.display?.replaceAll("_", " ")) ?? "----"}
              </option>
            );
          })}
        </select>
      )}
    />
  );
};

const BooleanFilter = (props: FilterWidgetProps<boolean>) => {
  const { label, value, onChange } = props;

  return (
    <FilterLayout
      label={label}
      block={(id) => (
        <input
          id={id}
          type="checkbox"
          checked={value}
          onChange={(it) => onChange(it.target.checked)}
        />
      )}
    />
  );
};

const FilterLayout = (
  props: DivPropsNoChildren<{
    label: string;
    block: (id: string) => ReactNode;
  }>,
) => {
  const { block, label, ...rest } = addClass(
    props,
    "flex items-center gap-x-2",
  );
  const id = useId();

  return (
    <div {...rest}>
      <label htmlFor={id} className="text-sm">
        {label}
      </label>
      {block(id)}
    </div>
  );
};
