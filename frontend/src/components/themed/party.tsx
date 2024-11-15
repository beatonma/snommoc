import type { Party } from "@/api";
import { ComponentPropsWithoutRef } from "react";
import { classes } from "@/util/react";
import { ThemedDiv } from "@/components/themed/themed-div";
import { resolveUrl } from "@/env";

interface PartyProps {
  party: Party | null;
}

const partyTheme = (party: Party) => ({
  primary: {
    backgroundColor: party.theme?.primary,
    color: party.theme?.on_primary,
  },
  accent: {
    backgroundColor: party.theme?.accent,
    color: party.theme?.on_accent,
  },
});

/**
 * Container with party primary theme.
 */
export const PartyPrimary = (
  props: PartyProps & ComponentPropsWithoutRef<"div">,
) => {
  const { party, ...rest } = props;
  if (!party) return <div {...rest} />;

  return (
    <ThemedDiv
      theme={partyTheme(party).primary}
      color={party.theme?.on_primary}
      {...rest}
    />
  );
};

/**
 * Container with party accent theme.
 */
export const PartyAccent = (
  props: PartyProps & ComponentPropsWithoutRef<"div">,
) => {
  const { party, ...rest } = props;
  if (!party) return <div {...rest} />;

  return (
    <ThemedDiv
      theme={partyTheme(party).accent}
      color={party.theme?.on_accent}
      {...rest}
    />
  );
};

export const PartyIconBackground = (
  props: PartyProps & ComponentPropsWithoutRef<"div">,
) => {
  const { party, className, children, ...rest } = props;
  if (!party)
    return (
      <div className={className} {...rest}>
        {children}
      </div>
    );
  if (!party?.logo)
    return (
      <PartyPrimary party={party} className={className} {...rest}>
        {children}
      </PartyPrimary>
    );

  return (
    <div
      className={classes(className, "relative overflow-hidden")}
      style={{
        color: party.theme?.on_primary,
      }}
      {...rest}
    >
      <div
        className="absolute inset-0 z-[-1] h-full w-full"
        style={{
          backgroundColor: party.theme?.primary,
        }}
      >
        <div
          className="inset-0 h-full w-full translate-x-1/2 bg-black opacity-[0.08] [mask-position:center] [mask-repeat:no-repeat] [mask-size:100%_auto]"
          style={{
            maskImage: `url('${resolveUrl(party.logo_mask ?? party.logo)}')`,
          }}
        />
      </div>
      {children}
    </div>
  );
};
