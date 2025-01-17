import React, { ReactNode } from "react";

interface HighlightProps {
  text: string;
  className: string;
}
export const Highlight = (props: HighlightProps & { pattern: RegExp }) => {
  const { text, pattern: _unsafePattern, className } = props;

  const safePattern = new RegExp(
    _unsafePattern.source,
    _unsafePattern.flags.includes("g")
      ? _unsafePattern.flags
      : _unsafePattern.flags + "g",
  );

  const parts: ReactNode[] = [];
  let lastIndex = 0;

  let match;
  while ((match = safePattern.exec(text)) !== null) {
    // Push the text before the match
    if (match.index > lastIndex) {
      parts.push(text.substring(lastIndex, match.index));
    }

    // Push the matched text wrapped in a span
    parts.push(
      <span key={match.index} className={className}>
        {match[0]}
      </span>,
    );

    lastIndex = safePattern.lastIndex;
  }

  // Push any remaining text after the last match
  if (lastIndex < text.length) {
    parts.push(text.substring(lastIndex));
  }

  return <>{parts}</>;
};

export const HighlightMoney = (props: HighlightProps) => (
  <Highlight pattern={/[£$][.,\d]+/} {...props} />
);
