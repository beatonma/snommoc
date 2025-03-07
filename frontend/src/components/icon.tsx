import { ComponentPropsWithoutRef } from "react";
import CommonsPersonIcon from "@/svg/commons-person.svg";
import CommonsTieIcon from "@/svg/commons-tie.svg";
import CommonsIcon from "@/svg/commons.svg";
import FacebookIcon from "@/svg/external/ic_facebook.svg";
import InstagramIcon from "@/svg/external/ic_instagram.svg";
import TwitterIcon from "@/svg/external/ic_twitter.svg";
import WikipediaIcon from "@/svg/external/ic_wikipedia.svg";
import CheckIcon from "@/svg/material/check.svg";
import CloseIcon from "@/svg/material/close.svg";
import FaxIcon from "@/svg/material/fax.svg";
import HomeIcon from "@/svg/material/home.svg";
import MailIcon from "@/svg/material/mail.svg";
import PhoneIcon from "@/svg/material/phone.svg";
import DarkModeIcon from "@/svg/material/theme_darkmode.svg";
import SystemDefaultThemeIcon from "@/svg/material/theme_default.svg";
import LightModeIcon from "@/svg/material/theme_lightmode.svg";
import { addClass } from "@/util/transforms";

const Icons = {
  Facebook: FacebookIcon,
  Twitter: TwitterIcon,
  Instagram: InstagramIcon,
  Wikipedia: WikipediaIcon,
  Check: CheckIcon,
  Close: CloseIcon,
  Phone: PhoneIcon,
  Email: MailIcon,
  Fax: FaxIcon,
  Home: HomeIcon,
  Commons: CommonsIcon,
  CommonsPerson: CommonsPersonIcon,
  CommonsTie: CommonsTieIcon,

  ThemeLightMode: LightModeIcon,
  ThemeDarkMode: DarkModeIcon,
  ThemeSystemDefault: SystemDefaultThemeIcon,
};
export type AppIcon = keyof typeof Icons;

export type IconProps = {
  icon?: AppIcon;
} & ComponentPropsWithoutRef<"svg">;
export const Icon = (props: IconProps) => {
  const { icon, ...rest } = addClass(props, "inline-block");
  if (!icon) return null;

  const Element = Icons[icon];
  if (!Element) throw `Unhandled icon: '${icon}'`;

  return <Element {...rest} />;
};
