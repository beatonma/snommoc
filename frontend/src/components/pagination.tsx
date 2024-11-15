import React, {
  ComponentPropsWithoutRef,
  ReactNode,
  useEffect,
  useRef,
  useState,
} from "react";
import { ApiPaginatedPromise } from "@/api";
import Loading from "@/components/loading";
import { TintedButton } from "@/components/button";

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

interface PaginationProps<T> {
  loader: PaginationLoader<T>;
  resetFlag?: boolean;
  itemComponent: (item: T) => ReactNode;
}

export const InfiniteScroll = <T,>(
  props: PaginationProps<T> & Omit<ComponentPropsWithoutRef<"div">, "children">,
) => {
  const { loader, resetFlag, itemComponent, ...rest } = props;
  const pagination = usePagination(loader);

  useEffect(() => {
    if (resetFlag === undefined) return;
    pagination.reset().then(() => pagination.loadNext?.());
  }, [resetFlag]);

  return (
    <div {...rest}>
      <div className="col-span-full col-start-1">
        {pagination.availableItems >= 0
          ? `${pagination.availableItems} results`
          : null}
      </div>

      {pagination.items.map((it) => itemComponent(it))}

      <LoadNext pagination={pagination} />
    </div>
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
      className="col-span-full col-start-1 flex justify-center p-16"
    >
      {content}
    </div>
  );
};
