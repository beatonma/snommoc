import type { components } from "./openapi";

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
export type Bill = schema["BillMiniSchema"];
export type BillDetail = schema["BillFullSchema"];
export type CommonsDivision = schema["CommonsDivisionSchema"];
export type LordsDivision = schema["LordsDivisionSchema"];
export type DivisionVoteType = schema["DivisionVoteType"];

const HouseTypeValues: HouseType[] = ["Commons", "Lords"];
const MemberStatusValues: StatusFilter[] = [
  "current",
  "inactive",
  "historical",
  "all",
];
const VoteTypes: DivisionVoteType[] = ["aye", "no", "did_not_vote"];
export const Fixtures = {
  HouseTypeValues,
  MemberStatusValues,
  VoteTypes,
};
