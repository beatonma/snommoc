import { Button } from "@/components/button";
import { NavDestination, navigationHref } from "@/navigation";
import { Props } from "@/types/react";

export const GlobalNavigation = () => (
  <nav>
    <ul className="list-none row-scroll items-center gap-y-2 gap-x-4 px-edge text-lg">
      <Destination destination="people">People</Destination>
      <Destination destination="parties">Parties</Destination>
      <Destination destination="constituencies">Constituencies</Destination>
      <Destination destination="nationalMap">Map</Destination>
      <Destination destination="divisions">Divisions</Destination>
    </ul>
  </nav>
);

const Destination = (
  props: Props<typeof Button, { destination: NavDestination }, "href">,
) => {
  const { destination, ...rest } = props;
  return (
    <li>
      <Button href={navigationHref(destination)} {...rest} />
    </li>
  );
};
