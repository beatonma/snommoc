import React, {
  ComponentPropsWithoutRef,
  ReactNode,
  useEffect,
  useRef,
  useState,
} from "react";
import { ApiPaginatedPromise, ExtraFilters } from "@/api";
import Loading from "@/components/loading";
import { TintedButton } from "@/components/button";
import { addClass, classes } from "@/util/transforms";

interface Paginated<T> {
  items: T[];
  availableItems: number;
  isLoading: boolean;
  hasMore: boolean;
  loadNext: (() => Promise<void>) | undefined;
  error: any | undefined;
  reset: () => Promise<void>;
}

export type PaginationLoader<T> = (
  offset?: number,
  query?: string,
  extraFilters?: ExtraFilters,
) => ApiPaginatedPromise<T>;

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

  const loadNext = async () => {
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
      const response = await loader(offset.current);

      const { data, error } = response;
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
  };

  useEffect(() => {
    void loadNext();
  }, []);

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

const FullSpan = "col-start-1 col-span-full";
export const InfiniteScroll = <T,>(
  props: PaginationProps<T> & Omit<ComponentPropsWithoutRef<"div">, "children">,
) => {
  const { loader, resetFlag, header, itemComponent, ...rest } = addClass(props);
  const pagination = usePagination(loader);

  useEffect(() => {
    if (resetFlag === undefined) return;
    pagination.reset().then(() => pagination.loadNext?.());
  }, [resetFlag]);

  return (
    <div {...rest}>
      {header}

      <GridSpan className="font-bold">
        {pagination.availableItems >= 0
          ? `${pagination.availableItems} results`
          : null}
      </GridSpan>

      {pagination.items.map((it, index, arr) => itemComponent(it, index, arr))}

      <LoadNext pagination={pagination} />
    </div>
  );
};

export const GridSpan = (props: ComponentPropsWithoutRef<"div">) => {
  const { className, ...rest } = props;
  return <div className={classes(className, FullSpan)} {...rest} />;
};
export const GridSpacer = (
  props: Omit<ComponentPropsWithoutRef<"div">, "children">,
) => {
  const { className, ...rest } = props;
  return <div className={classes(className, FullSpan)} {...rest} />;
};
export const GridSectionHeader = (props: ComponentPropsWithoutRef<"div">) => {
  const { className, ...rest } = props;
  return (
    <div
      className={classes(
        className,
        FullSpan,
        "text-md pt-4 text-center sm:text-start",
      )}
      {...rest}
    />
  );
};

const LoadNext = <T,>({ pagination }: { pagination: Paginated<T> }) => {
  const infiniteScrollingRef = useRef(null);

  useEffect(() => {
    const target = infiniteScrollingRef.current;
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries?.[0]?.isIntersecting) {
          void pagination.loadNext?.();
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
  }, [infiniteScrollingRef]);

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
      className={`${FullSpan} flex justify-center p-16`}
    >
      {content}
    </div>
  );
};
