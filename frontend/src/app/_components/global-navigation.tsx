import Link from "next/link";
import { NavDestination, navigationHref } from "@/navigation";
import { Props } from "@/types/react";

export const GlobalNavigation = () => (
  <nav>
    <ul className="list-none flex gap-y-2 gap-x-4 px-edge text-lg *:shrink-0 overflow-auto">
      <Destination destination="people">People</Destination>
      <Destination destination="parties">Parties</Destination>
      <Destination destination="constituencies">Constituencies</Destination>
      <Destination destination="nationalMap">Map</Destination>
      <Destination destination="divisions">Divisions</Destination>
    </ul>
  </nav>
);

const Destination = (
  props: Props<"a", { destination: NavDestination }, "href">,
) => {
  const { destination, ...rest } = props;
  return (
    <li className="hover text-center hover:text-primary">
      <Link
        className="block touch-target py-1 px-2"
        href={navigationHref(destination)}
        {...rest}
      />
    </li>
  );
};

const Separator = () => <div role="separator" className="hidden" />;
