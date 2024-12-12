import { ReactNode, useEffect, useState } from "react";
import { TintedButton } from "@/components/button";

type RemoteContentProvider = "openstreetmap.org";

const storageKeyOf = (provider: RemoteContentProvider) =>
  `remotecontentprovider__${provider}`;
const allowContentProvider = (provider: RemoteContentProvider): boolean => {
  return localStorage.getItem(storageKeyOf(provider))?.toLowerCase() === "true";
};

const setAllowContentProvider = (
  provider: RemoteContentProvider,
  allow: boolean,
) => {
  localStorage.setItem(storageKeyOf(provider), `${allow}`);
};

interface RemoteContentProps {
  provider: RemoteContentProvider;
  content: () => ReactNode;
}
export const RemoteContent = (props: RemoteContentProps) => {
  const { provider, content } = props;
  const [isAllowed, setIsAllowed] = useState<boolean>(
    allowContentProvider(provider),
  );

  useEffect(() => {
    setAllowContentProvider(provider, isAllowed);
  }, [provider, isAllowed]);

  if (isAllowed) {
    return <>{content()}</>;
  } else {
    return (
      <TintedButton onClick={() => setIsAllowed(true)}>
        {`Click to allow content from ${provider}`}
      </TintedButton>
    );
  }
};
