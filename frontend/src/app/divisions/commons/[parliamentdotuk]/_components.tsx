import type { DivisionVoteType } from "@/api";
import Icon, { AppIcon } from "@/components/icon";
import { classes } from "@/util/transforms";

export const MemberVoteIcon = (props: { vote: DivisionVoteType }) => {
  const icons: Record<DivisionVoteType, AppIcon> = {
    aye: "Upvote",
    no: "Downvote",
    did_not_vote: "DidNotVote",
  };
  const icon = icons[props.vote as DivisionVoteType];

  const theme: Record<DivisionVoteType, string> = {
    aye: "surface-positive",
    no: "surface-negative",
    did_not_vote: "surface-scrim",
  };

  return (
    <Icon
      icon={icon}
      className={classes(
        theme[props.vote],
        "size-6 p-1 border-[1px] border-current/60 rounded-md",
      )}
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
