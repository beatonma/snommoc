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

type MaybeString = string | undefined;
interface SingleChoiceFilter {
  title: string;
  value: MaybeString;
  values: MaybeString[];
}
export interface SearchFilters {
  singleChoice: Record<string, SingleChoiceFilter>;
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
    const serialized = serializeQuery(currentQuery, filtersQuery);
    /* Avoid reconstructing the loader if its query fields have not changed
     * in a meaningful way. */
    if (serialized === previous.current) return;
    previous.current = serialized;

    setLoader(
      () => (q: PaginatedQuery) =>
        propsLoader({
          query: currentQuery,
          ...filtersQuery,
          ...immutableFilters,
          ...q,
        }),
    );
  }, [propsLoader, immutableFilters, currentQuery, filtersQuery]);

  if (!loader) return <Loading />;

  return (
    <>
      <InfiniteScroll
        loader={loader}
        className={`${props.gridClassName ?? DefaultGridClass} my-2 mb-96 grid justify-center sm:mx-2`}
        header={
          <GridSpan
            className={`${props.header ? "md:justify-between" : "md:justify-center"} flex flex-wrap items-center justify-center`}
          >
            {props.header}
            <form
              className="flex items-center justify-center gap-2 p-4"
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

              <Filters filters={filters} setFilters={setFilters} />
            </form>
          </GridSpan>
        }
        itemComponent={props.itemComponent}
      />
    </>
  );
};

const useFilters = (
  init: SearchFilters | undefined,
): [SearchFilters, Dispatch<SetStateAction<SearchFilters>>, ExtraFilters] => {
  const [filters, setFilters] = useState(init ?? { singleChoice: {} });
  const [queryFilters, setQueryFilters] = useState({});

  useEffect(() => {
    const results: ExtraFilters = {};

    Object.entries(filters.singleChoice).forEach(([key, value]) => {
      results[key] = value.value || undefined;
    });
    setQueryFilters(results);
  }, [filters]);

  return [filters, setFilters, queryFilters];
};

const Filters = (props: {
  filters: SearchFilters;
  setFilters: (value: SearchFilters) => void;
}) => {
  const { filters, setFilters } = props;

  return (
    <div>
      {Object.entries(filters.singleChoice).map(([key, value]) => (
        <SingleChoiceFilter
          key={key}
          value={value.value}
          values={value.values}
          onChange={(it) => {
            const newFilters = { ...filters };
            newFilters["singleChoice"]![key]!["value"] = it;

            setFilters(newFilters);
          }}
        />
      ))}
    </div>
  );
};

interface SingleChoiceFilterProps {
  values: MaybeString[];
  value: MaybeString;
  onChange: (value: string) => void;
}
const SingleChoiceFilter = (props: SingleChoiceFilterProps) => {
  const { values, value, onChange } = props;

  return (
    <div className="">
      <select value={value} onChange={(it) => onChange(it.target.value)}>
        {values.map((opt) => (
          <option key={opt ?? null} value={opt ?? ""}>
            {opt ?? "----"}
          </option>
        ))}
      </select>
    </div>
  );
};

/**
 * Format query and any additional filters in a consistent, comparable way.
 */
const serializeQuery = (query: string, extras: ExtraFilters): string =>
  Object.entries({ query: query, ...extras })
    .map(([k, v]) => (v ? `${k}=${v}` : undefined))
    .filter(Boolean)
    .sort()
    .join(",");
