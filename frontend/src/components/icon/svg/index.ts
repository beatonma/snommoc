import BlueSky from "./external/ic_bluesky.svg";
import Facebook from "./external/ic_facebook.svg";
import Instagram from "./external/ic_instagram.svg";
import Twitter from "./external/ic_twitter.svg";
import Wikipedia from "./external/ic_wikipedia.svg";
import CommonsPerson from "./internal/commons-person.svg";
import CommonsTie from "./internal/commons-tie.svg";
import Commons from "./internal/commons.svg";
import Add from "./material/add.svg";
import ArrowDown from "./material/arrow_down.svg";
import ArrowUp from "./material/arrow_up.svg";
import Check from "./material/check.svg";
import Close from "./material/close.svg";
import Equal from "./material/equal.svg";
import Fax from "./material/fax.svg";
import Home from "./material/home.svg";
import Email from "./material/mail.svg";
import Phone from "./material/phone.svg";
import QuestionMark from "./material/questionmark.svg";
import Remove from "./material/remove.svg";
import ThemeDarkMode from "./material/theme_darkmode.svg";
import ThemeSystemDefault from "./material/theme_default.svg";
import ThemeLightMode from "./material/theme_lightmode.svg";

export const SvgIcons = {
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
  Upvote: Add,
  Downvote: Remove,
  DidNotVote: Equal,

  // General use
  Add,
  Remove,
  Equal,
  Check,
  Close,
  ArrowDown,
  ArrowUp,
  Home,
  QuestionMark,
};
export type AppIcon = keyof typeof SvgIcons;
export const isIcon = (name: string): boolean => name in SvgIcons;
