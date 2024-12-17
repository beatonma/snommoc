import client from "@/lib/api";
import { components, paths } from "@/lib/api/api";

export type ExtraFilters = Record<string, any>;
export type ApiFilters = paths[keyof paths]["get"]["parameters"]["query"];
export interface PaginatedQuery {
  offset?: number;
  limit?: number;
}

interface PaginatedData<T> {
  items: T[];
  count: number;
}
type ApiResponse<T> =
  | {
      data: T;
      error?: unknown;
      response: Response;
    }
  | {
      data?: T;
      error: unknown;
      response: Response;
    };

type ApiPromise<T> = Promise<ApiResponse<T>>;
export type ApiPaginatedPromise<T> = Promise<ApiResponse<PaginatedData<T>>>;

type schema = components["schemas"];

export type HouseType = schema["HouseType"];
export type StatusFilter = schema["StatusFilter"];

export type PartyDetail = schema["PartyFullSchema"];
export type GenderDemographics = schema["GenderDemographics"];
export type LordsDemographics = schema["LordsDemographics"];
export const getParty = async (
  parliamentdotuk: number,
): ApiPromise<PartyDetail> =>
  client.GET("/api/parties/{parliamentdotuk}/", {
    params: {
      path: {
        parliamentdotuk: parliamentdotuk,
      },
    },
  });

export type Party = schema["PartyMiniSchema"];
export type PartyTheme = schema["PartyThemeSchema"];
export type PartyFilters = paths["/api/parties/"]["get"]["parameters"]["query"];
export const getParties = async (
  query: PartyFilters,
): ApiPaginatedPromise<Party> =>
  client.GET("/api/parties/", {
    params: {
      query: query,
    },
  });

export type MemberProfile = schema["MemberProfile"];
export type MemberStatus = schema["MemberStatus"];
export type WebAddress = schema["WebAddressSchema"];
export const getMember = async (
  parliamentdotuk: number,
): ApiPromise<MemberProfile> =>
  client.GET("/api/members/{parliamentdotuk}/", {
    params: {
      path: {
        parliamentdotuk: parliamentdotuk,
      },
    },
  });

export type MemberMiniSchema = schema["MemberMiniSchema"];
export type MemberFilters =
  paths["/api/members/"]["get"]["parameters"]["query"];
export const getMembers = async (
  query: MemberFilters,
): ApiPaginatedPromise<MemberMiniSchema> =>
  client.GET("/api/members/", {
    params: {
      query: query,
    },
  });

export type ElectionResult = schema["ResultsSchema"];
export type Constituency = schema["ConstituencyFullSchema"];
export const getConstituency = async (
  parliamentdotuk: number,
): ApiPromise<Constituency> =>
  client.GET("/api/constituencies/{parliamentdotuk}/", {
    params: {
      path: {
        parliamentdotuk: parliamentdotuk,
      },
    },
  });

export type ConstituencyMini = schema["ConstituencyMiniSchema"];
export type ConstituencyFilters =
  paths["/api/constituencies/"]["get"]["parameters"]["query"];
export const getConstituencies = async (
  query: ConstituencyFilters,
): ApiPaginatedPromise<ConstituencyMini> =>
  client.GET("/api/constituencies/", {
    params: {
      query: query,
    },
  });

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
