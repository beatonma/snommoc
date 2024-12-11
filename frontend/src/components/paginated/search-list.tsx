import {
  GridSpan,
  InfiniteScroll,
  type PaginationItemComponent,
  PaginationLoader,
} from "@/components/paginated/pagination";
import React, {
  Dispatch,
  ReactNode,
  SetStateAction,
  useEffect,
  useId,
  useRef,
  useState,
} from "react";
import { useRouter, useSearchParams } from "next/navigation";
import {
  ApiPaginatedPromise,
  ExtraFilters,
  ApiFilters,
  PaginatedQuery,
} from "@/api";
import { TintedButton } from "@/components/button";
import Loading from "@/components/loading";
import { DivPropsNoChildren } from "@/types/react";
import { addClass, capitalize } from "@/util/transforms";
import { MaybeString } from "@/types/common";

const QueryParam = "query";
const DefaultGridClass =
  "grid-cols-[repeat(auto-fit,minmax(300px,400px))] gap-x-8 gap-y-4";

type SearchQuery = PaginatedQuery & ApiFilters;
type SearchLoader<T> = (query: SearchQuery) => ApiPaginatedPromise<T>;
interface ListPageProps<T> {
  loader: SearchLoader<T>;
  header?: ReactNode;
  itemComponent: PaginationItemComponent<T>;
  gridClassName?: string;

  /**
   * User-editable filters applied to search results.
   */
  searchFilters?: SearchFilters;

  /**
   * Filters that are always applied to search results.
   */
  immutableFilters?: ExtraFilters;
}

interface SearchFilter<T> {
  label: string;
  value: T;
}
interface FilterValue<T> {
  display: string;
  value: T;
}
interface SingleChoiceFilter extends SearchFilter<MaybeString> {
  values: (MaybeString | FilterValue<MaybeString>)[];
}
export interface SearchFilters {
  singleChoice: Record<string, SingleChoiceFilter>;
  bool: Record<string, SearchFilter<boolean>>;
}

export const SearchList = <T,>(props: ListPageProps<T>) => {
  const router = useRouter();
  const search = useSearchParams();
  const [query, setQuery] = useState<string>(search.get(QueryParam) ?? "");
  const [currentQuery, setCurrentQuery] = useState<string>(query);
  const [filters, setFilters, filtersQuery] = useFilters(props.searchFilters);
  const [loader, setLoader] = useState<PaginationLoader<T>>();
  const previous = useRef<string>();

  const { loader: propsLoader, immutableFilters } = props;

  useEffect(() => {
    /* Don't build loader until filtersQuery is populated. */
    if (filtersQuery == null) return;

    const serialized = serializeQuery(currentQuery, filtersQuery);
    /* Avoid reconstructing the loader if its query fields have not changed
     * in a meaningful way. */
    if (serialized === previous.current) return;
    previous.current = serialized;

    setLoader(
      () => (q: PaginatedQuery) =>
        propsLoader({
          query: currentQuery || undefined,
          ...filtersQuery,
          ...immutableFilters,
          ...q,
        }),
    );
  }, [propsLoader, immutableFilters, currentQuery, filtersQuery]);

  if (!loader) return <Loading />;

  const hasHeader = !!props.header;

  return (
    <>
      <InfiniteScroll
        loader={loader}
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
                action={() => {
                  router.push(`?${QueryParam}=${query}`);
                  setCurrentQuery(query);
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
    </>
  );
};

const useFilters = (
  init: SearchFilters | undefined,
): [
  SearchFilters,
  Dispatch<SetStateAction<SearchFilters>>,
  ExtraFilters | undefined,
] => {
  const [filters, setFilters] = useState(
    init ?? { singleChoice: {}, bool: {} },
  );
  const [queryFilters, setQueryFilters] = useState<ExtraFilters>();

  useEffect(() => {
    const results: ExtraFilters = {};

    Object.values(filters).forEach((filterType: SearchFilter<unknown>) => {
      Object.entries(filterType).forEach(([key, value]) => {
        results[key] = value.value || undefined;
        console.log(`-> ${key}=${value.value}`);
      });
    });
    setQueryFilters(results);
  }, [filters]);

  return [filters, setFilters, queryFilters];
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
      {Object.entries(filters.singleChoice).map(([key, value]) => (
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

      {Object.entries(filters.bool).map(([key, value]) => (
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
            const resolved =
              typeof opt === "string" ? { display: opt, value: opt } : opt;
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

/**
 * Format query and any additional filters in a consistent, comparable way.
 */
const serializeQuery = (query: string, extras: ExtraFilters): string =>
  Object.entries({ query: query, ...extras })
    .map(([k, v]) => (v ? `${k}=${v}` : undefined))
    .filter((it) => it != null)
    .sort()
    .join(",");
