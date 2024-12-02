import { ComponentPropsWithoutRef } from "react";
import { TextButton } from "@/components/button";

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
    Omit<ComponentPropsWithoutRef<"a">, "children" | "href" | "title">,
) => {
  const { licence: licenceKey, ...rest } = props;
  const licensing = licence(licenceKey);

  if (!licensing) throw new Error(`No licensing data for '${licenceKey}'`);

  return (
    <TextButton
      href={licensing.licence.url}
      title={licensing.licence.name}
      {...rest}
    >
      {licensing.attribution.join(" ")}
    </TextButton>
  );
};
