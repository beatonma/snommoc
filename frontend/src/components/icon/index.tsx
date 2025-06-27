import { Nullish } from "@/types/common";
import { Props } from "@/types/react";
import { AppIcon, SvgIcons } from "./svg";

export { type AppIcon };

export type IconProps = Props<
  "svg",
  {
    icon?: AppIcon | Nullish;
  }
>;

export default function Icon(props: IconProps) {
  const { icon, ...rest } = props;
  if (!icon) return null;

  const Element = SvgIcons[icon];
  if (!Element) throw `Unhandled icon: '${icon}'`;

  return <Element {...rest} />;
}

export const _private = {
  Icons: Object.keys(SvgIcons) as AppIcon[],
};
