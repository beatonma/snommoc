import parseHtml from "html-react-parser";
import React, { ReactNode, useMemo } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { XOR } from "@/types/common";

/** Common  */
export const HighlighterPatterns = {
  /* 2025-01-01 | 1 January 2025 | 01 January 2025 */
  Dates:
    /(\d{1,2} ((Jan|Febr)uary|March|April|May|Ju(ne|ly)|August|October|(Sept|Nov|Dec)ember) \d{4}|\d{4}-\d{2}-\d{2})/g,

  /* $100 | £100 | £1,000.50 */
  Money: /[£$][.,\d]+/g,
};

type Pattern = RegExp | keyof typeof HighlighterPatterns;
type ClassHighlighter = { className: string };
type BlockHighlighter = { block: (content: string) => ReactNode };
type ContentHighlighter = XOR<ClassHighlighter, BlockHighlighter>;
type HighlightProps = { text: string } & ContentHighlighter;
export type Highlighter = ContentHighlighter & {
  pattern: Pattern;
};
/**
 * Apply special formatting to any text that matches the given pattern.
 *
 * Examples:
 * <Highlight
 *     text={text}
 *     highlighters={[
 *       {
 *         pattern: "Dates",
 *         className: "text-yellow-500"
 *       },
 *     ]}
 * />
 */
export const Highlight = ({
  text,
  highlighters,
}: {
  text: string | null;
  highlighters: Highlighter[];
}) => {
  const highlightedText = useHighlighting(text, ...highlighters);

  return <>{highlightedText}</>;
};

const applyHighlighting = (props: HighlightProps & { pattern: Pattern }) => {
  const { text, pattern: patternOrKey, ...highlighter } = props;

  const pattern =
    patternOrKey instanceof RegExp
      ? patternOrKey
      : HighlighterPatterns[patternOrKey];
  if (!pattern.global) throw Error("Highlighter patterns must use /g flag.");

  const parts: ReactNode[] = [];
  let lastIndex = 0;
  let match;
  while ((match = pattern.exec(text)) !== null) {
    // Push the text before the match
    if (match.index > lastIndex) {
      parts.push(text.substring(lastIndex, match.index));
    }

    // Push the matched text wrapped with highlighter
    parts.push(renderToStaticMarkup(highlight(match[0], highlighter)));

    lastIndex = pattern.lastIndex;
  }

  // Push any remaining text after the last match
  if (lastIndex < text.length) {
    parts.push(text.substring(lastIndex));
  }

  return parts.join("");
};

const useHighlighting = (
  text: string | null,
  ...highlighters: Highlighter[]
): ReactNode => {
  return useMemo(() => {
    if (!text) return null;
    let highlightedText = text;

    for (const highlighter of highlighters) {
      highlightedText = applyHighlighting({
        text: highlightedText,
        ...highlighter,
      });
    }

    return parseHtml(highlightedText);
  }, [text, highlighters]);
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
