"use client";

import { useEffect, useState } from "react";
import { ApiPromise, Params, PathWithGet, ResponseOf, get } from "./client";

type useGetState<P extends PathWithGet> = ResponseOf<P> | "loading" | undefined;
export const useGet = <P extends PathWithGet>(
  path: P,
  params?: Params<P> | undefined,
  signal?: AbortSignal | undefined,
  getter: (
    path: P,
    query: Params<P>,
    signal?: AbortSignal,
  ) => ApiPromise<ResponseOf<P>> = get,
): useGetState<P> => {
  const [data, setData] = useState<useGetState<P>>("loading");

  useEffect(() => {
    getter(path, params ?? {}, signal).then((response) =>
      setData(response.data),
    );
  }, [getter, path, params, signal]);

  return data;
};
