import React, { ReactNode, useMemo } from "react";
import { XOR } from "@/types/common";

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

const resolvePattern = (patternOrKey: Pattern): RegExp => {
  const pattern: RegExp =
    patternOrKey instanceof RegExp
      ? patternOrKey
      : HighlighterPatterns[patternOrKey];
  if (!pattern.global) throw Error("Highlighter patterns must use /g flag.");
  return pattern;
};

const useHighlighting = (
  text: string | null,
  ...highlighters: Highlighter[]
): ReactNode => {
  return useMemo(() => {
    if (!text) return null;

    let segments: ReactNode[] = [text];

    highlighters.forEach((highlighter) => {
      const newSegments: ReactNode[] = [];
      const pattern = resolvePattern(highlighter.pattern);

      segments.forEach((segment) => {
        if (typeof segment === "string") {
          let lastIndex = 0;
          let match;

          while ((match = pattern.exec(segment)) !== null) {
            const matchedText = match[0];
            const startIndex = match.index;
            const endIndex = pattern.lastIndex;

            // Push the matched text wrapped with highlighter
            if (startIndex > lastIndex) {
              newSegments.push(segment.substring(lastIndex, startIndex));
            }

            // Apply highlighting
            newSegments.push(
              <React.Fragment key={`${startIndex}-${endIndex}`}>
                {highlight(matchedText, highlighter)}
              </React.Fragment>,
            );

            lastIndex = endIndex;
          }

          // Push any remaining text after the last match
          if (lastIndex < segment.length) {
            newSegments.push(segment.substring(lastIndex));
          }
        } else {
          newSegments.push(segment);
        }
      });
      segments = newSegments;
    });

    return <React.Fragment>{segments}</React.Fragment>;
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
