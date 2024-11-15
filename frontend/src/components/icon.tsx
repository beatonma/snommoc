import FacebookIcon from "@/svg/external/ic_facebook.svg";
import TwitterIcon from "@/svg/external/ic_twitter.svg";
import CommonsIcon from "@/svg/commons.svg";
import PhoneIcon from "@/svg/material/phone.svg";
import MailIcon from "@/svg/material/mail.svg";
import FaxIcon from "@/svg/material/fax.svg";
import { ComponentPropsWithoutRef } from "react";

const Icons = {
  Facebook: FacebookIcon,
  Twitter: TwitterIcon,
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
  const { icon, ...rest } = props;
  if (!icon) return null;

  const Element = Icons[icon];
  if (!Element) throw `Unhandled icon: '${icon}'`;

  return <Element className="fill-white" {...rest} />;
};
