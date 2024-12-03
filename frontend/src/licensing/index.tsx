import { ComponentPropsWithoutRef, ReactNode } from "react";
import { StyledLink } from "@/components/link";

interface Licence {
  name: string;
  url: string;
}

interface Licensing {
  licence: Licence;
  attribution: string[];
}

const Licensing = {
  OpenParliament: {
    licence: {
      name: "Open Parliament Licence v3.0",
      url: "https://www.parliament.uk/site-information/copyright-parliament/open-parliament-licence/",
    },
    attribution: [
      "Contains Parliamentary information licensed under the Open Parliament Licence v3.0.",
    ],
  },
};

export const licence = (licence: keyof typeof Licensing) => {
  return Licensing[licence];
};

interface LicenseProps {
  licence: keyof typeof Licensing;
}
export const License = (
  props: LicenseProps &
    Omit<ComponentPropsWithoutRef<"div">, "children" | "title">,
) => {
  const { licence: licenceKey, ...rest } = props;
  const licensing = licence(licenceKey);

  if (!licensing) throw new Error(`No licensing data for '${licenceKey}'`);

  return (
    <div {...rest}>
      <LinkifiedAttribution {...licensing} />
    </div>
  );
};

const LinkifiedAttribution = (props: Licensing) => {
  const { licence, attribution } = props;

  if (!attribution.find((it) => it.includes(licence.name))) {
    // If licence name not included in attribution text, linkify the whole text.
    return (
      <StyledLink href={licence.url} title={licence.name}>
        {attribution.map((attr, index) => (
          <p key={index}>{attr}</p>
        ))}
      </StyledLink>
    );
  }

  // Otherwise, linkify the licence name wherever it appears
  const linkified = (
    <StyledLink href={licence.url} title={licence.name}>
      {licence.name}
    </StyledLink>
  );

  return (
    <>
      {attribution.map((attr) => {
        const parts = attr
          .split(licence.name)
          .map((fragment, index) =>
            fragment ? <span key={index}>{fragment}</span> : "",
          );

        const lastIndex = parts.length - 1;
        const results: ReactNode[] = [];
        parts.forEach((part, index) => {
          results.push(part);
          if (index < lastIndex) {
            results.push(linkified);
          }
        });

        return <p key={attr}>{results}</p>;
      })}
    </>
  );
};
