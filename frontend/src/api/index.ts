import client from "@/lib/api";
import { components } from "@/lib/api/api";

interface PaginatedData<T> {
  items: T[];
  count: number;
}
type ApiResponse<T> =
  | {
      data: T;
      error?: unknown;
    }
  | {
      data?: T;
      error: unknown;
    };

type ApiPromise<T> = Promise<ApiResponse<T>>;
export type ApiPaginatedPromise<T> = Promise<ApiResponse<PaginatedData<T>>>;

export type PartyDetail = components["schemas"]["PartyFullSchema"];
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

export type Party = components["schemas"]["PartyMiniSchema"];
export const getParties = async (offset?: number): ApiPaginatedPromise<Party> =>
  client.GET("/api/parties/", {
    params: {
      query: { offset: offset },
    },
  });

export type MemberProfile = components["schemas"]["MemberProfile"];
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

export type MemberMiniSchema = components["schemas"]["MemberMiniSchema"];
export const getMembers = async (
  offset?: number,
  query?: string,
): ApiPaginatedPromise<MemberMiniSchema> =>
  client.GET("/api/members/", {
    params: {
      query: { offset: offset, query: query },
    },
  });

export type ConstituencyMini = components["schemas"]["ConstituencyMiniSchema"];
