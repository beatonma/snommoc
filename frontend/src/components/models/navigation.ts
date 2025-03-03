type Navigable = "party" | "constituency" | "person";
const Navigation: Record<Navigable, (parliamentdotuk: number) => string> = {
  constituency: (parliamentdotuk) => `/constituencies/${parliamentdotuk}/`,
  party: (parliamentdotuk) => `/parties/${parliamentdotuk}/`,
  person: (parliamentdotuk) => `/members/${parliamentdotuk}/`,
};

export const navigationHref = (
  type: Navigable,
  parliamentdotuk: number,
): string => Navigation[type](parliamentdotuk);
