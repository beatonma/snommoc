import { InfiniteScroll, PaginationLoader } from "@/components/pagination";
import React, { ReactNode, useEffect, useRef, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

interface ListPageProps<T> {
  loader: PaginationLoader<T>;
  itemComponent: (item: T) => ReactNode;
  gridClassName?: string;
}
const QueryParam = "query";
const DefaultGridClass =
  "grid-cols-[repeat(auto-fit,minmax(300px,400px))] gap-x-8 gap-y-4";

export const SearchListPage = <T,>(props: ListPageProps<T>) => {
  const router = useRouter();
  const search = useSearchParams();
  const [query, setQuery] = useState<string>(search.get(QueryParam) ?? "");
  const activeQuery = useRef(query);
  const [resetFlag, setResetFlag] = useState<boolean>();

  useEffect(() => {
    const q = search.get(QueryParam) ?? "";
    if (q === activeQuery.current) return;
    setQuery(q);
    activeQuery.current = q;
    setResetFlag((it) => !it);
  }, [search]);

  return (
    <main>
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
        <button type="submit">Search</button>
      </form>

      <InfiniteScroll
        loader={(offset) => props.loader(offset, activeQuery.current)}
        resetFlag={resetFlag}
        className={`${props.gridClassName ?? DefaultGridClass} m-2 mb-96 grid justify-center`}
        itemComponent={props.itemComponent}
      />
    </main>
  );
};
