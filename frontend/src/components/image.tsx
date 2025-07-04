import { StaticImport } from "next/dist/shared/lib/get-img-props";
import { ImageProps, default as NextImage } from "next/image";
import React from "react";
import { Nullish } from "@/types/common";
import { DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";

interface OptionalImage {
  src: string | StaticImport | undefined | null;
}
type OptionalImageProps = Omit<ImageProps, keyof OptionalImage> & OptionalImage;
export const OptionalImage = (props: OptionalImageProps) => {
  const { src, ...rest } = props;
  if (src) {
    return <NextImage src={src} {...rest} />;
  }
};

export const OptionalSvg = (props: OptionalImageProps) => (
  <OptionalImage {...props} width={1} height={1} />
);

export const MaskedSvg = (
  props: DivPropsNoChildren<{ src: string | Nullish }>,
) => (
  <div
    {...addClass(
      props,
      "[mask-position:center] [mask-repeat:no-repeat] [mask-size:100%_auto]",
    )}
    style={{ maskImage: `url('${props.src}')`, ...props.style }}
  />
);
