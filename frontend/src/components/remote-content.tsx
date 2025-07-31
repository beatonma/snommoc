"use client";

import { ReactNode, useEffect, useState } from "react";
import { TintedButton } from "@/components/button";
import { LoadingSpinner } from "@/components/loading";

export interface RemoteContentProvider {
  domain: string;
  description: ReactNode;
}

interface RemoteContentProps {
  provider: RemoteContentProvider;
  content: () => ReactNode;
}
export const RemoteContent = (
  props: RemoteContentProps & {
    permissionUi?: (button: ReactNode) => ReactNode;
  },
) => {
  const { provider, content, permissionUi } = props;
  const [isAllowed, setIsAllowed] = useState<boolean>();

  useEffect(() => {
    if (isAllowed === undefined) {
      setIsAllowed(getSavedPreference(provider));
      return;
    }

    setSavedPreference(provider, isAllowed);
  }, [provider, isAllowed]);

  if (isAllowed === undefined) return <LoadingSpinner />;
  if (isAllowed) return <>{content()}</>;

  const button = (
    <TintedButton
      onClick={() => setIsAllowed(true)}
      className="self-center place-self-center"
    >
      Click to allow content from {provider.domain}
    </TintedButton>
  );

  if (permissionUi) {
    return permissionUi(button);
  }
  return button;

  // const { children, ...rest } = permissionProps ?? {};
  // return (
  //   <div {...addClass(rest, "relative flex")}>
  //     <div className="absolute size-full">{children}</div>
  //     <TintedButton
  //       onClick={() => setIsAllowed(true)}
  //       className="self-center place-self-center"
  //     >
  //       Click to allow content from {provider.domain}
  //     </TintedButton>
  //   </div>
  // );
};

const storageKeyOf = (provider: RemoteContentProvider) =>
  `remotecontentprovider__${provider.domain}`;

const getSavedPreference = (provider: RemoteContentProvider): boolean =>
  window.localStorage.getItem(storageKeyOf(provider))?.toLowerCase() === "true";

const setSavedPreference = (
  provider: RemoteContentProvider,
  allow: boolean,
) => {
  window.localStorage.setItem(storageKeyOf(provider), `${allow}`);
};
