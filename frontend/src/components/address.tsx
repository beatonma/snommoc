import api from "@/lib/api/api";
import { OptionalDiv } from "@/components/optional";
import { TextButton } from "@/components/button";
import type { AppIcon } from "@/components/icon";
import { ComponentPropsWithoutRef } from "react";

type PhysicalAddress = api.components["schemas"]["PhysicalAddressSchema"];
export const PhysicalAddress = (
  props: PhysicalAddress & ComponentPropsWithoutRef<"address">,
) => {
  const { description, address, postcode, phone, fax, email, ...rest } = props;
  return (
    <address {...rest}>
      <OptionalDiv className="text-xs" condition={description} />
      <div className="py-0.5">
        <OptionalDiv condition={address} />
        <OptionalDiv condition={postcode} />
      </div>
      <OptionalDiv
        condition={phone}
        block={(it) => (
          <TextButton icon="Phone" href={`tel:${it}`}>
            {it}
          </TextButton>
        )}
      />
      <OptionalDiv
        condition={fax}
        block={(it) => (
          <TextButton icon="Fax" href={`tel:${it}`}>
            {it}
          </TextButton>
        )}
      />
      <OptionalDiv
        condition={email}
        block={(it) => (
          <TextButton icon="Email" href={`mailto:${it}`}>
            {it}
          </TextButton>
        )}
      />
    </address>
  );
};

type WebAddress = api.components["schemas"]["WebAddressSchema"];
export const WebAddress = (
  props: WebAddress & ComponentPropsWithoutRef<"address">,
) => {
  const { url, description, ...rest } = props;
  const [displayText, icon] = webDisplayValues(url);

  return (
    <address {...rest}>
      <TextButton
        icon={icon}
        href={url}
        title={description ?? undefined}
        target="_blank"
        referrerPolicy="same-origin"
      >
        {displayText ?? description}
      </TextButton>
    </address>
  );
};

interface WebHost {
  pattern: RegExp;
  icon: AppIcon;
  displayText: string;
}
const Username = "{username}";
const WebHosts: WebHost[] = [
  {
    pattern: /(https:\/\/)?(www\.)?(x|twitter)\.com\/(?<username>\w+)/g,
    icon: "Twitter",
    displayText: Username,
  },
  {
    pattern: /(https:\/\/)?(www\.)?facebook\.com\/(?<username>\w+)/g,
    icon: "Facebook",
    displayText: Username,
  },
  {
    pattern: /(https:\/\/)?(www\.)?instagram\.com\/(?<username>\w+)/g,
    icon: "Instagram",
    displayText: Username,
  },
];
const webDisplayValues = (
  url: string,
): [string | undefined, AppIcon | undefined] => {
  let displayText: string | undefined = undefined;
  let icon: AppIcon | undefined = undefined;
  for (const host of WebHosts) {
    const username = host.pattern.exec(url)?.groups?.["username"];

    if (username) {
      displayText = host.displayText.replace(Username, username);
      icon = host.icon;
      break;
    }
  }

  if (!displayText) {
    const niceUrl = URL.parse(url)?.hostname?.replace("www.", "");
    if (niceUrl) {
      displayText = niceUrl;
    }
  }

  return [displayText, icon];
};
