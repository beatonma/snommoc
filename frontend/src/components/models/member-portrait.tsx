import Image from "next/image";
import React from "react";
import Icon from "@/components/icon";
import { classes } from "@/util/transforms";

interface PortraitProps {
  name: string;
  className?: string;
  aspectClassName?: string; // Used if src is useful, otherwise use square aspect for default image
  src?: string | null | undefined;
}
export const MemberPortrait = (props: PortraitProps) => {
  const { className, aspectClassName, name, src } = props;

  return (
    <div
      className={classes(
        className,
        aspectClassName,
        "relative size-full max-h-[173px] max-w-[260px]", // Size from api source
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
        <Icon icon="Commons" className="size-full" />
      )}
    </div>
  );
};
