import React, {
  Dispatch,
  ReactNode,
  SetStateAction,
  useCallback,
  useEffect,
  useId,
  useRef,
  useState,
} from "react";
import { useRouter, useSearchParams } from "next/navigation";
import {
  type _DeprExtraFilters,
  type SearchablePath,
  type PageItemType,
  type Query,
} from "@/api";
import { TintedButton } from "@/components/button";
import { DivPropsNoChildren } from "@/types/react";
import { addClass, capitalize } from "@/util/transforms";
import { MaybeString } from "@/types/common";
import { InfiniteScroll, PaginationItemComponent } from "./infinite-scroll";
import { GridSpan } from "@/components/grid";

const QueryParam = "query";
const DefaultGridClass =
  "grid-cols-[repeat(auto-fit,var(--spacing-listitem_card))] gap-x-8 gap-y-4";

export interface SearchFilters {
  singleChoice?: Record<string, SingleChoiceFilter>;
  bool?: Record<string, SearchFilter<boolean>>;
}

interface ListPageProps<P extends SearchablePath> {
  path: P;
  query?: Query<P> | undefined;
  header?: ReactNode;
  itemComponent: PaginationItemComponent<PageItemType<P>>;
  gridClassName?: string;

  /**
   * User-editable filters applied to search results.
   */
  searchFilters?: SearchFilters;

  /**
   * Filters that are always applied to search results.
   */
  immutableFilters?: _DeprExtraFilters;
}
export const SearchList = <P extends SearchablePath>(
  props: ListPageProps<P>,
) => {
  const { path, query: queryFromProps, immutableFilters } = props;

  const router = useRouter();
  const search = useSearchParams();
  const [query, setQuery] = useState<string>(search.get(QueryParam) ?? "");
  const [currentQuery, setCurrentQuery] = useState<string>(query);
  const [filters, setFilters, filtersQuery] = useFilters(
    props.searchFilters,
    search,
  );
  const [composedQuery, setComposedQuery] = useState<Query<P> | undefined>();

  const previousSearchParams = useRef<string>(undefined);
  const isInitialized = useRef<boolean>(false);

  const updateSearchParams = useCallback(
    /**
     * Update the browser location to reflect current state of query and filters.
     * Return true if there was a meaningful change.
     */
    (query: string, filters: _DeprExtraFilters): boolean => {
      const params = new URLSearchParams();
      Object.entries({ [QueryParam]: query, ...filters }).forEach(
        ([key, value]) => {
          if (value != null && value !== "") {
            params.set(key, value);
          }
        },
      );
      params.sort();
      const serialized = `${params}`;
      if (serialized === previousSearchParams.current) return false;
      previousSearchParams.current = serialized;
      if (isInitialized.current) {
        router.push(`?${serialized}`);
      } else {
        router.replace(`?${serialized}`);
      }
      return true;
    },
    [router],
  );

  useEffect(() => {
    /**
     * When navigating back/forward, update the active query from browser location.
     */
    const q = search.get(QueryParam) ?? "";
    if (q === currentQuery) return;
    setQuery(q);
    setCurrentQuery(q);
  }, [search, updateSearchParams]);

  useEffect(() => {
    /* Don't build loader until filtersQuery is populated. */
    if (filtersQuery == null) return;

    const paramsChanged = updateSearchParams(currentQuery, filtersQuery);
    if (!paramsChanged) return;

    const fullQuery: Query<P> = {
      query: currentQuery,
      ...filtersQuery,
      ...immutableFilters,
    };
    setComposedQuery(fullQuery);
    isInitialized.current = true;
  }, [
    updateSearchParams,
    queryFromProps,
    immutableFilters,
    currentQuery,
    filtersQuery,
  ]);

  if (composedQuery === undefined) return;

  return (
    <_SearchList
      path={path}
      composedQuery={composedQuery}
      header={props.header}
      gridClassName={props.gridClassName}
      itemComponent={props.itemComponent}
      searchQuery={query}
      setSearchQuery={setQuery}
      onConfirmSearch={() => setCurrentQuery(query)}
      filters={filters}
      setFilters={setFilters}
    />
  );
};

const _SearchList = <P extends SearchablePath>(props: {
  path: P;
  composedQuery: Query<P> | undefined;
  header: ReactNode | undefined;
  itemComponent: PaginationItemComponent<PageItemType<P>>;
  gridClassName: string | undefined;
  searchQuery: string;
  setSearchQuery: (q: string) => void;
  onConfirmSearch: () => void;
  filters: SearchFilters;
  setFilters: (value: SearchFilters) => void;
}) => {
  const hasHeader = !!props.header;

  return (
    <InfiniteScroll
      path={props.path}
      query={props.composedQuery}
      itemComponent={props.itemComponent}
      className={`${props.gridClassName ?? DefaultGridClass} my-2 mb-96 grid justify-center sm:mx-2`}
      header={
        <GridSpan
          className={`${hasHeader ? "md:justify-between" : "md:justify-center"} flex flex-wrap items-center justify-center`}
        >
          {props.header}

          <div
            className={`flex max-w-[600px] flex-col items-center gap-4 p-4 ${hasHeader ? "md:items-end" : ""}`}
          >
            <form
              className="flex items-center justify-center gap-2"
              action={() => props.onConfirmSearch()}
            >
              <input
                type="search"
                value={props.searchQuery}
                onChange={(e) => props.setSearchQuery(e.target.value)}
              />
              <TintedButton type="submit">Search</TintedButton>
            </form>

            <Filters
              filters={props.filters}
              setFilters={props.setFilters}
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
const useFilters = (
  init: SearchFilters | undefined,
  initUrlParams: URLSearchParams,
): [
  SearchFilters,
  Dispatch<SetStateAction<SearchFilters>>,
  _DeprExtraFilters | undefined,
] => {
  const [filters, setFilters] = useState<SearchFilters>(() =>
    initFilters(init, initUrlParams),
  );
  const [queryFilters, setQueryFilters] = useState<_DeprExtraFilters>();

  useEffect(() => {
    // Build a flat {key:value} map suitable for use in URLSearchParams.
    const results: _DeprExtraFilters = {};

    Object.values(filters).forEach((filterType: SearchFilter<unknown>) => {
      Object.entries(filterType).forEach(([key, value]) => {
        results[key] = value.value || undefined;
      });
    });
    setQueryFilters(results);
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
  props: {
    filters: SearchFilters;
    setFilters: (value: SearchFilters) => void;
  } & DivPropsNoChildren,
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
                {capitalize(resolved?.display) ?? "----"}
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
  props: DivPropsNoChildren & {
    label: string;
    block: (id: string) => ReactNode;
  },
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
