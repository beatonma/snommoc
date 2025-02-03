import React, {
  ReactNode,
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";
import { ApiPaginatedPromise, PaginatedQuery } from "@/api";
import Loading from "@/components/loading";
import { TintedButton } from "@/components/button";
import { addClass } from "@/util/transforms";
import { DivProps, DivPropsNoChildren } from "@/types/react";
import { plural } from "@/util/plurals";
import WindowInsets from "@/components/insets";

const FullSpan = "col-start-1 col-span-full";

export type PaginationLoader<T> = (
  query: PaginatedQuery,
) => ApiPaginatedPromise<T>;

export type PaginationItemComponent<T> = (
  item: T,
  index: number,
  arr: T[],
) => ReactNode;
interface PaginationProps<T> {
  header?: ReactNode;
  loader: PaginationLoader<T>;
  resetFlag?: boolean;
  itemComponent: PaginationItemComponent<T>;
}

export const InfiniteScroll = <T,>(
  props: PaginationProps<T> & DivPropsNoChildren,
) => {
  const { loader, resetFlag, header, itemComponent, ...rest } = props;
  const pagination = usePagination(loader);

  useEffect(() => {
    if (resetFlag === undefined) return;
    pagination.reset().then(() => pagination.loadNext?.());
  }, [pagination, resetFlag]);

  return (
    <div {...rest}>
      {header}

      <GridSpan className={`${WindowInsets} font-bold`}>
        {pagination.availableItems >= 0
          ? plural("result", pagination.availableItems)
          : null}
      </GridSpan>

      {pagination.items.map((it, index, arr) => itemComponent(it, index, arr))}

      <LoadNext pagination={pagination} />
    </div>
  );
};

export const GridSpan = (props: DivProps) => {
  return <div {...addClass(props, FullSpan)} />;
};
export const GridSpacer = (props: DivPropsNoChildren) => {
  return <div {...addClass(props, FullSpan)} />;
};
export const GridSectionHeader = (props: DivProps) => {
  return (
    <div
      {...addClass(props, FullSpan, "text-md pt-4 text-center sm:text-start")}
    />
  );
};

interface Paginated<T> {
  items: T[];
  availableItems: number;
  isLoading: boolean;
  hasMore: boolean;
  loadNext: (() => Promise<void>) | undefined;
  error: any | undefined;
  reset: () => Promise<void>;
}
const usePagination = <T,>(loader: PaginationLoader<T>): Paginated<T> => {
  const [items, setItems] = useState<T[]>([]);
  const [error, setError] = useState<any>();
  const totalItemsAvailable = useRef(-1);
  const offset = useRef(0);
  const [isLoading, setIsLoading] = useState(false);
  const loadingRef = useRef(false);

  const reset = async () => {
    setItems([]);
    setError(undefined);
    setIsLoading(false);
    totalItemsAvailable.current = -1;
    offset.current = 0;
    loadingRef.current = false;
  };

  const loadNext = useCallback(async () => {
    if (loadingRef.current) return;
    if (
      totalItemsAvailable.current >= 0 &&
      offset.current >= totalItemsAvailable.current
    )
      return;

    loadingRef.current = true;
    setIsLoading(true);
    setError(undefined);

    try {
      const { data, error, response } = await loader({
        offset: offset.current,
      });

      if (error || !data) {
        setError(error);
        return;
      }

      setItems((prev) => [...prev, ...data.items]);
      totalItemsAvailable.current = data.count;
      offset.current = offset.current + data.items.length;
    } catch (e: unknown) {
      setError(e);
    } finally {
      setIsLoading(false);
      loadingRef.current = false;
    }
  }, [loader]);

  useEffect(() => {
    reset().then(loadNext);
  }, [loadNext]);

  return {
    items: items,
    availableItems: totalItemsAvailable.current,
    isLoading: isLoading,
    error: error,
    reset: reset,
    loadNext: loadNext,
    hasMore: offset.current < totalItemsAvailable.current,
  };
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
  if (!pagination.hasMore) content = null;
  else if (pagination.isLoading) content = <Loading />;
  else if (pagination.loadNext)
    content = (
      <TintedButton onClick={pagination.loadNext}>Load more</TintedButton>
    );
  else content = null;

  return (
    <div
      ref={infiniteScrollingRef}
      className={`${FullSpan} m-16 flex justify-center`}
    >
      {content}
    </div>
  );
};
