import { ComponentPropsWithoutRef } from "react";
import CommonsPersonIcon from "./svg/commons-person.svg";
import CommonsTieIcon from "./svg/commons-tie.svg";
import CommonsIcon from "./svg/commons.svg";
import BlueSkyIcon from "./svg/external/ic_bluesky.svg";
import FacebookIcon from "./svg/external/ic_facebook.svg";
import InstagramIcon from "./svg/external/ic_instagram.svg";
import TwitterIcon from "./svg/external/ic_twitter.svg";
import WikipediaIcon from "./svg/external/ic_wikipedia.svg";
import CheckIcon from "./svg/material/check.svg";
import CloseIcon from "./svg/material/close.svg";
import FaxIcon from "./svg/material/fax.svg";
import HomeIcon from "./svg/material/home.svg";
import MailIcon from "./svg/material/mail.svg";
import PhoneIcon from "./svg/material/phone.svg";
import DarkModeIcon from "./svg/material/theme_darkmode.svg";
import SystemDefaultThemeIcon from "./svg/material/theme_default.svg";
import LightModeIcon from "./svg/material/theme_lightmode.svg";

const Icons = {
  // First party
  Commons: CommonsIcon,
  CommonsPerson: CommonsPersonIcon,
  CommonsTie: CommonsTieIcon,

  // Third party
  BlueSky: BlueSkyIcon,
  Facebook: FacebookIcon,
  Instagram: InstagramIcon,
  Twitter: TwitterIcon,
  Wikipedia: WikipediaIcon,

  // App UI
  ThemeLightMode: LightModeIcon,
  ThemeDarkMode: DarkModeIcon,
  ThemeSystemDefault: SystemDefaultThemeIcon,

  // Communications
  Email: MailIcon,
  Fax: FaxIcon,
  Phone: PhoneIcon,

  // General use
  Check: CheckIcon,
  Close: CloseIcon,
  Home: HomeIcon,
};
export type AppIcon = keyof typeof Icons;

export type IconProps = {
  icon?: AppIcon;
} & ComponentPropsWithoutRef<"svg">;

export default function Icon(props: IconProps) {
  const { icon, ...rest } = props;
  if (!icon) return null;

  const Element = Icons[icon];
  if (!Element) throw `Unhandled icon: '${icon}'`;

  return <Element {...rest} />;
}
