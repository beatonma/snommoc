import React, { ReactNode } from "react";
import { Date } from "@/components/datetime";

type ClassHighlighter = { className: string };
type BlockHighlighter = { block: (content: string) => ReactNode };
type ContentHighlighter = ClassHighlighter | BlockHighlighter;
type HighlightProps = { text: string } & ContentHighlighter;
export const Highlight = (props: HighlightProps & { pattern: RegExp }) => {
  const { text, pattern: _unsafePattern, ...highlighter } = props;

  if (!text) return null;

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

    // Push the matched text wrapped with highlighter
    parts.push(highlight(match[0], highlighter));

    lastIndex = safePattern.lastIndex;
  }

  // Push any remaining text after the last match
  if (lastIndex < text.length) {
    parts.push(text.substring(lastIndex));
  }

  return <>{parts}</>;
};

const highlight = (
  content: string,
  highlighter: ContentHighlighter,
): ReactNode => {
  if ("className" in highlighter) {
    return <span className={highlighter.className}>{content}</span>;
  }
  if ("block" in highlighter) {
    return highlighter.block(content);
  }

  throw new Error(`Unknown highlighter ${highlighter}`);
};

export const HighlighterPatterns = {
  Dates:
    /\d{1,2} ((Jan|Febr)uary|March|April|May|Ju(ne|ly)|August|October|(Sept|Nov|Dec)ember) \d{4}/g,
  Money: /[£$][.,\d]+/g,
};

export const HighlightMoney = (props: HighlightProps) => (
  <Highlight pattern={HighlighterPatterns.Money} {...props} />
);
export const HighlightDates = (props: {
  text: string;
  dateFormat?: Intl.DateTimeFormatOptions;
  className?: string;
}) => {
  return (
    <Highlight
      pattern={HighlighterPatterns.Dates}
      text={props.text}
      block={(it) => (
        <Date
          dateFormat={props.dateFormat}
          date={it}
          className={props.className}
        />
      )}
    />
  );
};
