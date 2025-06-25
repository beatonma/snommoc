import { ComponentPropsWithoutRef } from "react";
import { Nullish } from "@/types/common";
import CommonsPerson from "./svg/commons-person.svg";
import CommonsTie from "./svg/commons-tie.svg";
import Commons from "./svg/commons.svg";
import BlueSky from "./svg/external/ic_bluesky.svg";
import Facebook from "./svg/external/ic_facebook.svg";
import Instagram from "./svg/external/ic_instagram.svg";
import Twitter from "./svg/external/ic_twitter.svg";
import Wikipedia from "./svg/external/ic_wikipedia.svg";
import ArrowDown from "./svg/material/arrow_down.svg";
import ArrowUp from "./svg/material/arrow_up.svg";
import CaretDown from "./svg/material/caret_down.svg";
import CaretUp from "./svg/material/caret_up.svg";
import Check from "./svg/material/check.svg";
import Close from "./svg/material/close.svg";
import Fax from "./svg/material/fax.svg";
import Home from "./svg/material/home.svg";
import Email from "./svg/material/mail.svg";
import NoChange from "./svg/material/no_change.svg";
import Phone from "./svg/material/phone.svg";
import QuestionMark from "./svg/material/questionmark.svg";
import ThemeDarkMode from "./svg/material/theme_darkmode.svg";
import ThemeSystemDefault from "./svg/material/theme_default.svg";
import ThemeLightMode from "./svg/material/theme_lightmode.svg";

const Icons = {
  // First party
  Commons,
  CommonsPerson,
  CommonsTie,

  // Third party
  BlueSky,
  Facebook,
  Instagram,
  Twitter,
  Wikipedia,

  // App UI
  ThemeLightMode,
  ThemeDarkMode,
  ThemeSystemDefault,

  // Communications
  Email,
  Fax,
  Phone,

  // Votes
  Upvote: CaretUp,
  Downvote: CaretDown,
  DidNotVote: NoChange,

  // General use
  ArrowUp,
  ArrowDown,
  Check,
  Close,
  Home,
  QuestionMark,
};
export type AppIcon = keyof typeof Icons;

export type IconProps = {
  icon?: AppIcon | Nullish;
} & ComponentPropsWithoutRef<"svg">;

export default function Icon(props: IconProps) {
  const { icon, ...rest } = props;
  if (!icon) return null;

  const Element = Icons[icon];
  if (!Element) throw `Unhandled icon: '${icon}'`;

  return <Element {...rest} />;
}

export const _private = {
  Icons: Object.keys(Icons) as AppIcon[],
};
