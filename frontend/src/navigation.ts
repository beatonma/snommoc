import { HouseType } from "@/api/schema";

const Navigation = {
  bill: (parliamentdotuk: number) => `/bills/${parliamentdotuk}/`,
  bills: () => `/bills/`,
  constituencies: () => "/constituencies/",
  constituency: (parliamentdotuk: number) =>
    `/constituencies/${parliamentdotuk}/`,
  division: (house: HouseType, parliamentdotuk: number) =>
    `/divisions/${house.toLowerCase()}/${parliamentdotuk}/`,
  divisions: () => "/divisions/",
  nationalMap: () => "/maps/",
  organisation: (slug: string) => `/organisations/${slug}/`,
  organisations: () => `/organisations/`,
  parties: () => "/parties/",
  party: (parliamentdotuk: number) => `/parties/${parliamentdotuk}/`,
  people: () => "/members/",
  person: (parliamentdotuk: number) => `/members/${parliamentdotuk}/`,
};
type Navigable = keyof typeof Navigation;
export type NavDestination = {
  [K in Navigable]: (typeof Navigation)[K] extends () => string ? K : never;
}[Navigable];

export const navigationHref = <T extends Navigable>(
  type: T,
  ...args: Parameters<(typeof Navigation)[T]>
): string => {
  type P = (...args: Parameters<(typeof Navigation)[T]>) => string;
  return (Navigation[type] as P)(...args);
};
