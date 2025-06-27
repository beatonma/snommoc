import { notFound } from "next/navigation";
import type { PathsWithMethod } from "openapi-typescript-helpers";
import client from "@/lib/api";
import type { components, paths } from "@/lib/api/api";

type schema = components["schemas"];

// Commonly used types
export type HouseType = schema["HouseType"];
export type StatusFilter = schema["StatusFilter"];
export type PartyDetail = schema["PartyFullSchema"];
export type GenderDemographics = schema["GenderDemographics"];
export type LordsDemographics = schema["LordsDemographics"];
export type Party = schema["PartyMiniSchema"];
export type ItemTheme = schema["ItemThemeSchema"];
export type MemberProfile = schema["MemberProfile"];
export type PhysicalAddress = schema["PhysicalAddressSchema"];
export type WebAddress = schema["WebAddressSchema"];
export type MemberCareer = schema["MemberCareerHistory"];
export type MemberMiniSchema = schema["MemberMiniSchema"];
export type ElectionResult = schema["ResultsSchema"];
export type Constituency = schema["ConstituencyFullSchema"];
export type ConstituencyMini = schema["ConstituencyMiniSchema"];
export type ConstituencyMiniBoundary = schema["ConstituencyMapSchema"];
export type PartyTerritory = schema["PartyMapSchema"];
export type Organisation = schema["OrganisationSchema"];
export type Post = Omit<schema["PostSchema"], "start" | "end">;
export type Committee = Omit<schema["CommitteeMemberSchema"], "start" | "end">;
export type Division = schema["DivisionMiniSchema"];
export type CommonsDivision = schema["CommonsDivisionSchema"];
export type LordsDivision = schema["LordsDivisionSchema"];
export type DivisionVoteType = schema["DivisionVoteType"];

// eslint-disable-next-line @typescript-eslint/no-namespace
export namespace Fixtures {
  export const HouseTypeValues: HouseType[] = ["Commons", "Lords"];
  export const MemberStatusValues: StatusFilter[] = [
    "current",
    "inactive",
    "historical",
    "all",
  ];
  export const VoteTypes: DivisionVoteType[] = ["aye", "no", "did_not_vote"];
}

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
type ApiPromise<T> = Promise<ApiResponse<T>>;

export type Path = keyof paths;
export type Query<P extends Path> =
  paths[P]["get"]["parameters"]["query"] extends never
    ? never
    : paths[P]["get"]["parameters"]["query"];

export type PathWithGet = PathsWithMethod<paths, "get">;
export type Params<P extends PathWithGet> = paths[P]["get"]["parameters"];

export const get = async <P extends PathWithGet>(
  path: P,
  params?: Params<P>,
  signal?: AbortSignal,
) =>
  client.GET(
    path,
    // @ts-expect-error Unable to find 'correct' type for this object
    {
      params,
      signal,
    },
  );

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

export type PagedResponseOf<P extends PathWithPagination> = paths[P] extends {
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
