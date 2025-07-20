import parseHtml, {
  DOMNode,
  Element,
  HTMLReactParserOptions,
  attributesToProps,
  domToReact,
} from "html-react-parser";
import { ReactNode, useMemo } from "react";
import { InlineButton } from "@/components/button";
import { onlyIf } from "@/components/optional";
import { Nullish } from "@/types/common";

type HtmlOptions = Pick<
  HTMLReactParserOptions,
  "replace" | "transform" | "trim"
>;
export const useHtml = (
  html: string | Nullish,
  options: HtmlOptions = defaultOptions,
): ReactNode => {
  return useMemo(
    () => onlyIf(html, (it) => parseHtml(it, options)),
    [html, options],
  );
};

export const Html = (props: { html: string | Nullish }) => {
  const html = useHtml(props.html);

  return <>{html}</>;
};

const defaultOptions: HtmlOptions = {
  replace: (domNode) => {
    if (domNode.type === "tag") {
      switch (domNode.tagName) {
        case "a":
          const attrs = attributesToProps(domNode.attribs);
          return (
            <InlineButton {...attrs}>
              {domToReact(domNode.children as DOMNode[], defaultOptions)}
            </InlineButton>
          );

        case "p":
          if (!domNode.children.length) return <></>;

          // If <p> only contains <br> children, remove the <p>.
          if (
            domNode.children.length === 1 &&
            (domNode.children[0] as Element).tagName === "br"
          ) {
            return <></>;
          }
          break;

        case "br":
          if (!domNode.previousSibling && !domNode.nextSibling) return <></>;

          return <span className="break" />;
      }
    }
  },
};
