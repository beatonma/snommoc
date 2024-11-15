import client from "@/lib/api";
import { components } from "@/lib/api/api";

export type PartyDetail = components["schemas"]["PartyFullSchema"];
export const getParty = (parliamentdotuk: number) =>
  client.GET("/api/parties/{parliamentdotuk}/", {
    params: {
      path: {
        parliamentdotuk: parliamentdotuk,
      },
    },
  });

export type Party = components["schemas"]["PartyMiniSchema"];
export const getParties = (offset?: number) =>
  client.GET("/api/parties/", {
    params: {
      query: { offset: offset },
    },
  });

export type MemberProfile = components["schemas"]["MemberProfile"];
export const getMember = (parliamentdotuk: number) =>
  client.GET("/api/members/{parliamentdotuk}/", {
    params: {
      path: {
        parliamentdotuk: parliamentdotuk,
      },
    },
  });

export type MemberMiniSchema = components["schemas"]["MemberMiniSchema"];
export const getMembers = (offset?: number) =>
  client.GET("/api/members/", {
    params: {
      query: { offset: offset },
    },
  });

export type ConstituencyMini = components["schemas"]["ConstituencyMiniSchema"];
