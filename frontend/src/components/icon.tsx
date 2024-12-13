import FacebookIcon from "@/svg/external/ic_facebook.svg";
import TwitterIcon from "@/svg/external/ic_twitter.svg";
import InstagramIcon from "@/svg/external/ic_instagram.svg";
import WikipediaIcon from "@/svg/external/ic_wikipedia.svg";
import CommonsIcon from "@/svg/commons.svg";
import HomeIcon from "@/svg/material/home.svg";
import PhoneIcon from "@/svg/material/phone.svg";
import MailIcon from "@/svg/material/mail.svg";
import FaxIcon from "@/svg/material/fax.svg";
import { ComponentPropsWithoutRef } from "react";
import { addClass, classes } from "@/util/transforms";

const Icons = {
  Facebook: FacebookIcon,
  Twitter: TwitterIcon,
  Instagram: InstagramIcon,
  Wikipedia: WikipediaIcon,
  Phone: PhoneIcon,
  Email: MailIcon,
  Fax: FaxIcon,
  Home: HomeIcon,
  Commons: CommonsIcon,
};
export type AppIcon = keyof typeof Icons;

interface IconProps {
  icon?: AppIcon;
}
export const Icon = (props: IconProps & ComponentPropsWithoutRef<"svg">) => {
  const { icon, ...rest } = addClass(props, "inline-block");
  if (!icon) return null;

  const Element = Icons[icon];
  if (!Element) throw `Unhandled icon: '${icon}'`;

  return <Element {...rest} />;
};
