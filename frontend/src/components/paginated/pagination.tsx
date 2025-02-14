import { useCallback, useEffect, useRef, useState } from "react";
import {
  getPaginated,
  PageItemType,
  type PathWithPagination,
  type Query,
} from "@/api";

export interface Paginated<T> {
  items: T[];
  availableItems: number;
  isLoading: boolean;
  hasMore: boolean;
  loadNext: (() => Promise<void>) | undefined;
  error: any | undefined;
  reset: () => Promise<void>;
}

export const usePagination = <P extends PathWithPagination>(
  path: P,
  query?: Query<P> | undefined,
): Paginated<PageItemType<P>> => {
  const [items, setItems] = useState<PageItemType<P>[]>([]);
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
      const fullQuery: Query<P> = {
        ...((query ?? {}) as Query<P>),
        offset: offset.current,
      };
      const {
        data,
        error: err,
        response,
      } = await getPaginated(path, fullQuery);

      if (err || !data) {
        setError(err);
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
  }, [path, query]);

  useEffect(() => {
    console.log(`reset ${path} ${JSON.stringify(query)}`);
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
