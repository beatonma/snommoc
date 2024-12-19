import FacebookIcon from "@/svg/external/ic_facebook.svg";
import TwitterIcon from "@/svg/external/ic_twitter.svg";
import InstagramIcon from "@/svg/external/ic_instagram.svg";
import WikipediaIcon from "@/svg/external/ic_wikipedia.svg";
import CloseIcon from "@/svg/material/close.svg";
import CommonsIcon from "@/svg/commons.svg";
import CommonsPersonIcon from "@/svg/commons-person.svg";
import CommonsTieIcon from "@/svg/commons-tie.svg";
import HomeIcon from "@/svg/material/home.svg";
import PhoneIcon from "@/svg/material/phone.svg";
import MailIcon from "@/svg/material/mail.svg";
import FaxIcon from "@/svg/material/fax.svg";
import { ComponentPropsWithoutRef } from "react";
import { addClass } from "@/util/transforms";

const Icons = {
  Facebook: FacebookIcon,
  Twitter: TwitterIcon,
  Instagram: InstagramIcon,
  Wikipedia: WikipediaIcon,
  Close: CloseIcon,
  Phone: PhoneIcon,
  Email: MailIcon,
  Fax: FaxIcon,
  Home: HomeIcon,
  Commons: CommonsIcon,
  CommonsPerson: CommonsPersonIcon,
  CommonsTie: CommonsTieIcon,
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
