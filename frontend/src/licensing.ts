interface LicenceDefinition {
  name: string;
  url: string;
  attribution: string[];
}

const Licences: Record<string, LicenceDefinition> = {
  OpenParliament: {
    name: "Open Parliament Licence v3.0",
    url: "https://www.parliament.uk/site-information/copyright-parliament/open-parliament-licence/",
    attribution: [
      "Contains Parliamentary information licensed under the Open Parliament Licence v3.0.",
    ],
  },
};

export const licence = (licence: keyof typeof Licences) => {
  return Licences[licence];
};
export type Licence = keyof typeof Licences;
