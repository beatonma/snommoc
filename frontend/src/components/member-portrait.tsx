import Image from "next/image";
import React from "react";
import CommonsIcon from "@/svg/commons.svg";
import { classes } from "@/util/transforms";

interface PortraitProps {
  name: string;
  className?: string;
  aspectClassName?: string; // Used if src is useful, otherwise use square aspect for default image
  src?: string | null | undefined;
}
export const MemberPortrait = (props: PortraitProps) => {
  const { className, aspectClassName = "aspect-square", name, src } = props;

  return (
    <div
      className={classes(
        className,
        src ? aspectClassName : "aspect-square",
        "relative max-h-[173px] max-w-[260px]", // Size from api source
      )}
    >
      {src ? (
        <Image
          fill
          loading="lazy"
          src={src}
          alt={`Portrait of ${name}`}
          sizes="260px" // Size from api source
        />
      ) : (
        <CommonsIcon className="size-full" />
      )}
    </div>
  );
};
