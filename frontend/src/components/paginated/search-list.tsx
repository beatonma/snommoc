import {
  GridSpan,
  InfiniteScroll,
  type PaginationItemComponent,
  PaginationLoader,
} from "@/components/paginated/pagination";
import React, { ReactNode, useEffect, useRef, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { ExtraFilters } from "@/api";
import { TintedButton } from "@/components/button";
import { Optional } from "@/components/optional";

interface ListPageProps<T> {
  loader: PaginationLoader<T>;
  header?: ReactNode;
  itemComponent: PaginationItemComponent<T>;
  gridClassName?: string;
  extraFilters?: ExtraFilters;
}
const QueryParam = "query";
const DefaultGridClass =
  "grid-cols-[repeat(auto-fit,minmax(300px,400px))] gap-x-8 gap-y-4";

export const SearchList = <T,>(props: ListPageProps<T>) => {
  const router = useRouter();
  const search = useSearchParams();
  const [query, setQuery] = useState<string>(search.get(QueryParam) ?? "");
  const activeQuery = useRef(query);
  const [resetFlag, setResetFlag] = useState<boolean>();

  useEffect(() => {
    const q = search.get(QueryParam) ?? "";
    if (q === activeQuery.current) return;
    activeQuery.current = q;
    setQuery(q);
    setResetFlag((it) => !it);
  }, [search]);

  return (
    <div>
      <InfiniteScroll
        loader={(offset) =>
          props.loader(offset, activeQuery.current, props.extraFilters)
        }
        resetFlag={resetFlag}
        className={`${props.gridClassName ?? DefaultGridClass} my-2 mb-96 grid justify-center sm:mx-2`}
        header={
          <GridSpan
            className={`${props.header ? "md:justify-between" : "md:justify-center"} flex flex-wrap items-center justify-center`}
          >
            {props.header}
            <form
              className="flex justify-center gap-2 p-4"
              action={() => {
                activeQuery.current = query;
                router.push(`?${QueryParam}=${query}`);
                setResetFlag((it) => !it);
              }}
            >
              <input
                type="search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              <TintedButton type="submit">Search</TintedButton>
            </form>
          </GridSpan>
        }
        itemComponent={props.itemComponent}
      />
    </div>
  );
};
