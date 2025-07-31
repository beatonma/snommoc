"use client";

import { default as NextImage } from "next/image";
import React, { ReactNode, useState } from "react";
import { Nullish } from "@/types/common";
import { DivPropsNoChildren, Props } from "@/types/react";
import { addClass } from "@/util/transforms";

type NextImageSrc = Props<typeof NextImage>["src"];
type OptionalImageProps = Props<
  typeof NextImage,
  { src: NextImageSrc | Nullish }
>;

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

export const ImageWithFallback = (
  props: OptionalImageProps & { fallback: ReactNode },
) => {
  const { src: preferredSrc, fallback, ...rest } = props;

  const [src, setSrc] = useState(preferredSrc);

  if (src) {
    return (
      <NextImage
        src={src}
        onError={() => {
          if (typeof fallback === "string") {
            setSrc(fallback);
          } else {
            setSrc(undefined);
          }
        }}
        {...rest}
      />
    );
  }

  return <>{fallback}</>;
};
