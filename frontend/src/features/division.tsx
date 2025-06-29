import { DivisionVoteType } from "@/api/schema";
import Icon, { AppIcon, IconProps } from "@/components/icon";
import { addClass } from "@/util/transforms";

export const MemberVoteIcon = (
  props: Omit<IconProps<{ vote: DivisionVoteType }>, "icon">,
) => {
  const { vote, ...rest } = props;
  const icons: Record<DivisionVoteType, AppIcon> = {
    aye: "Upvote",
    no: "Downvote",
    did_not_vote: "DidNotVote",
  };
  const icon = icons[vote as DivisionVoteType];

  const theme: Record<DivisionVoteType, string> = {
    aye: "surface-positive",
    no: "surface-negative",
    did_not_vote: "surface-scrim",
  };

  return (
    <Icon
      icon={icon}
      {...addClass(rest, theme[vote])}
      // className={classes(
      //   theme[vote],
      //   "size-6 p-1 border-[1px] border-current/60 rounded-md",
      // )}
    />
  );
};

export const MemberVoteDescription = (props: { vote: DivisionVoteType }) => {
  const descriptions: Record<DivisionVoteType, string> = {
    aye: "Voted in favour",
    no: "Voted against",
    did_not_vote: "Did not vote",
  };
  return descriptions[props.vote] ?? descriptions["did_not_vote"];
};
