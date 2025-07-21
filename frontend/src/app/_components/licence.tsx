import React from "react";
import { InlineLink } from "@/components/button";
import { Highlight } from "@/components/highlight";
import { Licence, licence } from "@/licensing";
import { DivPropsNoChildren } from "@/types/react";

interface LicenseProps {
  licence: Licence;
}
export const License = (props: DivPropsNoChildren<LicenseProps, "title">) => {
  const { licence: licenceKey, ...rest } = props;
  const licensing = licence(licenceKey);

  if (!licensing) throw new Error(`No licensing data for '${licenceKey}'`);

  return (
    <div {...rest}>
      {licensing.attribution.map((it, index) => (
        <Highlight
          key={`${licensing.name}-${index}`}
          text={it}
          highlighters={[
            {
              pattern: new RegExp(licensing.name, "g"),
              block: (it) => <InlineLink href={licensing.url}>{it}</InlineLink>,
            },
          ]}
        />
      ))}
    </div>
  );
};
