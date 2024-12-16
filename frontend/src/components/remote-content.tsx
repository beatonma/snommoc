"use client";

import { ReactNode, useEffect, useState } from "react";
import { TintedButton } from "@/components/button";
import Loading from "@/components/loading";

type RemoteContentProvider = "openstreetmap.org";

interface RemoteContentProps {
  provider: RemoteContentProvider;
  content: () => ReactNode;
}
export const RemoteContent = (props: RemoteContentProps) => {
  const { provider, content } = props;
  const [isAllowed, setIsAllowed] = useState<boolean>();

  useEffect(() => {
    if (isAllowed === undefined) {
      setIsAllowed(getSavedPreference(provider));
      return;
    }

    setSavedPreference(provider, isAllowed);
  }, [provider, isAllowed]);

  if (isAllowed === undefined) return <Loading />;
  if (isAllowed) return <>{content()}</>;

  return (
    <TintedButton onClick={() => setIsAllowed(true)}>
      {`Click to allow content from ${provider}`}
    </TintedButton>
  );
};

const storageKeyOf = (provider: RemoteContentProvider) =>
  `remotecontentprovider__${provider}`;
const getSavedPreference = (provider: RemoteContentProvider): boolean =>
  window.localStorage.getItem(storageKeyOf(provider))?.toLowerCase() === "true";

const setSavedPreference = (
  provider: RemoteContentProvider,
  allow: boolean,
) => {
  window.localStorage.setItem(storageKeyOf(provider), `${allow}`);
};
