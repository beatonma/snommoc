import FacebookIcon from "@/svg/external/ic_facebook.svg";
import TwitterIcon from "@/svg/external/ic_twitter.svg";
import InstagramIcon from "@/svg/external/ic_instagram.svg";
import CommonsIcon from "@/svg/commons.svg";
import PhoneIcon from "@/svg/material/phone.svg";
import MailIcon from "@/svg/material/mail.svg";
import FaxIcon from "@/svg/material/fax.svg";
import { ComponentPropsWithoutRef } from "react";
import { classes } from "@/util/react";

const Icons = {
  Facebook: FacebookIcon,
  Twitter: TwitterIcon,
  Instagram: InstagramIcon,
  Phone: PhoneIcon,
  Email: MailIcon,
  Fax: FaxIcon,
  Commons: CommonsIcon,
};
export type AppIcon = keyof typeof Icons;

interface IconProps {
  icon?: AppIcon;
}
export const Icon = (props: IconProps & ComponentPropsWithoutRef<"svg">) => {
  const { icon, className, ...rest } = props;
  if (!icon) return null;

  const Element = Icons[icon];
  if (!Element) throw `Unhandled icon: '${icon}'`;

  return <Element className={classes(className)} {...rest} />;
};
