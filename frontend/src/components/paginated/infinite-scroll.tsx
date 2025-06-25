import React, { ReactNode, useEffect, useRef } from "react";
import { PageItemType, PathWithPagination } from "@/api";
import { TintedButton } from "@/components/button";
import { GridSpan } from "@/components/grid";
import Loading from "@/components/loading";
import { DivPropsNoChildren } from "@/types/react";
import { plural } from "@/util/plurals";
import { type Paginated } from "./pagination";

export type PaginationItemComponent<T> = (
  item: T,
  index: number,
  arr: T[],
) => ReactNode;

interface PaginationProps<P extends PathWithPagination> {
  header?: ReactNode;
  pagination: Paginated<PageItemType<P>>;
  resetFlag?: boolean;
  itemComponent: PaginationItemComponent<PageItemType<P>>;
}
export const InfiniteScroll = <P extends PathWithPagination>(
  props: PaginationProps<P> & DivPropsNoChildren,
) => {
  const { pagination, resetFlag, header, itemComponent, ...rest } = props;

  useEffect(() => {
    if (resetFlag === undefined) return;
    pagination.reset().then(() => pagination.loadNext?.());
  }, [pagination, resetFlag]);

  return (
    <div {...rest}>
      {header}

      <GridSpan className="px-edge font-bold">
        {pagination.availableItems >= 0
          ? plural("result", pagination.availableItems)
          : null}
      </GridSpan>

      {pagination.items.map((it, index, arr) => itemComponent(it, index, arr))}

      <LoadNext pagination={pagination} />
    </div>
  );
};

const LoadNext = <T,>({ pagination }: { pagination: Paginated<T> }) => {
  const infiniteScrollingRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const target = infiniteScrollingRef.current;
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            void pagination.loadNext?.();
            return;
          }
        }
      },
      { threshold: 1 },
    );

    if (target) {
      observer.observe(target);
    }

    return () => {
      if (target) {
        observer.unobserve(target);
      }
    };
  }, [pagination, infiniteScrollingRef]);

  let content;
  if (pagination.error) {
    content = <h2>ERROR</h2>;
    console.error(pagination.error);
  } else if (pagination.isLoading) content = <Loading />;
  else if (pagination.hasMore && pagination.loadNext) {
    content = (
      <TintedButton onClick={pagination.loadNext}>Load more</TintedButton>
    );
  } else content = null;

  return (
    <GridSpan ref={infiniteScrollingRef} className="m-16 flex justify-center">
      {content}
    </GridSpan>
  );
};
