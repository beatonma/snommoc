import client from "@/lib/api";
import { type components, type paths } from "@/lib/api/api";
import { FilterKeys } from "openapi-typescript-helpers";
import { FetchOptions } from "openapi-fetch";

type schema = components["schemas"];

// Commonly used types
export type HouseType = schema["HouseType"];
export type StatusFilter = schema["StatusFilter"];
export type PartyDetail = schema["PartyFullSchema"];
export type GenderDemographics = schema["GenderDemographics"];
export type LordsDemographics = schema["LordsDemographics"];
export type Party = schema["PartyMiniSchema"];
export type PartyTheme = schema["PartyThemeSchema"];
export type MemberProfile = schema["MemberProfile"];
export type PhysicalAddress = schema["PhysicalAddressSchema"];
export type WebAddress = schema["WebAddressSchema"];
export type MemberCareer = schema["MemberCareerHistory"];
export type MemberMiniSchema = schema["MemberMiniSchema"];
export type ElectionResult = schema["ResultsSchema"];
export type Constituency = schema["ConstituencyFullSchema"];
export type ConstituencyMini = schema["ConstituencyMiniSchema"];
export type ConstituencyMap = schema["ConstituencyMapSchema"];
export type PartyTerritory = schema["PartyMapSchema"];
export type Organisation = schema["OrganisationSchema"];
export type Post = Omit<schema["PostSchema"], "start" | "end">;
export type Committee = Omit<schema["CommitteeMemberSchema"], "start" | "end">;

// eslint-disable-next-line @typescript-eslint/no-namespace
export namespace Fixtures {
  export const HouseTypeValues: HouseType[] = ["Commons", "Lords"];
  export const MemberStatusValues: StatusFilter[] = [
    "current",
    "inactive",
    "historical",
    "all",
  ];
}

export type _DeprExtraFilters = Record<string, any>;

interface Paged<T> {
  items: T[];
  count: number;
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
type ApiPromise<T> = Promise<ApiResponse<T>>;

export type Path = keyof paths;
export type Query<P extends Path> =
  paths[P]["get"]["parameters"]["query"] extends never
    ? never
    : paths[P]["get"]["parameters"]["query"];
export type PathArgs<P extends Path> =
  paths[P]["get"]["parameters"]["path"] extends never
    ? never
    : paths[P]["get"]["parameters"]["path"];

type GetInit<Path extends keyof paths> = FetchOptions<
  FilterKeys<paths[Path], "get">
>;
export const get = <P extends Path>(
  path: P,
  params?: { path?: PathArgs<P>; query?: Query<P> }, // todo RequiredKeysOf
): ApiPromise<ResponseOf<P>> =>
  client.GET(path, {
    params: params,
  } as GetInit<P>) as ApiPromise<ResponseOf<P>>;

export const getPaginated = <P extends PathWithPagination>(
  path: P,
  query: Query<P>,
): ApiPromise<PagedResponseOf<P>> =>
  client.GET(path, {
    params: {
      query: query,
    },
  } as GetInit<P>) as ApiPromise<PagedResponseOf<P>>;

export type ResponseOf<P extends Path> = paths[P] extends {
  get: {
    responses: {
      200: {
        content: {
          "application/json": infer JSON;
        };
      };
    };
  };
}
  ? JSON
  : never;

type PagedResponseOf<P extends PathWithPagination> = paths[P] extends {
  get: {
    responses: {
      200: {
        content: {
          "application/json": Paged<unknown>;
        };
      };
    };
  };
}
  ? Paged<PageItemType<P>>
  : never;

export type PageItemType<P extends PathWithPagination> =
  paths[P]["get"]["responses"][200]["content"]["application/json"] extends {
    items: (infer ItemType)[];
  }
    ? ItemType
    : never;

/**
 * Paths which returns a Paged response.
 */
export type PathWithPagination = {
  [Path in keyof paths]: paths[Path] extends {
    get: {
      responses: {
        200: {
          content: {
            "application/json": Paged<unknown>;
          };
        };
      };
    };
  }
    ? Path
    : never;
}[keyof paths];

/**
 * Paths which accept a ?query=string parameter.
 */
type PathWithSearch = {
  [Path in keyof paths]: paths[Path] extends {
    get: {
      parameters: infer Parameters;
    };
  }
    ? Parameters extends { query?: never }
      ? never
      : Parameters extends { query?: { query?: string } }
        ? Path
        : never
    : never;
}[keyof paths];
export type SearchablePath = PathWithPagination & PathWithSearch;
