import { notFound } from "next/navigation";
import createClient, { Middleware } from "openapi-fetch";
import { PathsWithMethod } from "openapi-typescript-helpers";
import * as env from "@/env";
import type { paths } from "./openapi";

const authMiddleware: Middleware = {
  async onRequest({ request }) {
    request.headers.set("Authorization", env.SNOMMOC_API_KEY);
    return request;
  },
};

const client = createClient<paths>({
  baseUrl: process.env.SERVER ?? window.location.origin,
});
client.use(authMiddleware);
export default client;

export const get = async <P extends PathWithGet>(
  path: P,
  params?: Params<P>,
  signal?: AbortSignal,
): ApiPromise<ResponseOf<P>> =>
  client.GET(
    path,
    // @ts-expect-error Unable to find 'correct' type for this object
    {
      params,
      signal,
    },
  ) as ApiPromise<ResponseOf<P>>;

export const getOrNull = async <P extends PathWithGet>(
  path: P,
  params?: Params<P>,
  signal?: AbortSignal,
) => {
  const response = await get(path, params, signal);
  const data = response.data;

  return data ?? null;
};

export const getOr404 = async <P extends PathWithGet>(
  path: P,
  params?: Params<P>,
  signal?: AbortSignal,
) => {
  const data = await getOrNull(path, params, signal);

  if (!data) return notFound();
  return data;
};

export const getPaginated = <P extends PathWithPagination>(
  path: P,
  query: Params<P>,
  signal?: AbortSignal,
): ApiPromise<PagedResponseOf<P>> =>
  get(path, query, signal) as ApiPromise<PagedResponseOf<P>>;

interface Paged<T> {
  items: T[];
  count: number;
  previous: number | null;
  next: number | null;
}
type ApiResponse<T> =
  | {
      data: T;
      error?: never;
      response: Response;
    }
  | {
      data?: never;
      error: unknown;
      response: Response;
    };
export type ApiPromise<T> = Promise<ApiResponse<T>>;
type GetResponse200<T> = { get: { responses: { 200: T } } };
type GetResponse200Json<T> = GetResponse200<{
  content: { "application/json": T };
}>;

export type Path = keyof paths;
export type PathWithGet = PathsWithMethod<paths, "get">;
export type Params<P extends PathWithGet> = paths[P]["get"]["parameters"];
export type Query<P extends PathWithGet> = Params<P>["query"];

/** Union of all paths which extend T */
type PathsOf<T> = {
  [P in Path]: paths[P] extends T ? P : never;
}[Path];

/** Paths which return a JSON response of T */
type PathWithGetResponse200Json<T> = PathsOf<GetResponse200Json<T>>;

/** Paths which return a JSON response of Paged<T> */
export type PathWithPaginationOf<T> = PathWithGetResponse200Json<Paged<T>>;
/** Paths which returns a Paged response of any kind.*/
export type PathWithPagination = PathWithPaginationOf<unknown>;

/** Return the type of the JSON data returned by the given path. */
export type ResponseOf<P extends Path> =
  paths[P] extends GetResponse200Json<infer JSON> ? JSON : never;

export type PagedResponseOf<P extends PathWithPagination> =
  paths[P] extends GetResponse200Json<Paged<unknown>>
    ? Paged<PageItemType<P>>
    : never;

/** Return the type of items in the paginated response of the given path. */
export type PageItemType<P extends PathWithPagination> =
  paths[P] extends GetResponse200Json<Paged<infer ItemType>> ? ItemType : never;

/**
 * Paths which accept a ?query=string parameter.
 */
type PathWithSearch = {
  [P in PathWithGet]: Params<P> extends { query?: { query?: string } }
    ? P
    : never;
}[Path];
export type SearchablePath = PathWithPagination & PathWithSearch;
