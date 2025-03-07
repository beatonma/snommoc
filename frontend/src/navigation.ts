const Navigation = {
  constituencies: () => "/constituencies/",
  constituency: (parliamentdotuk: number) =>
    `/constituencies/${parliamentdotuk}/`,
  nationalMap: () => "/maps/",
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
