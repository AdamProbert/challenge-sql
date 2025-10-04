import { useMemo } from "react";
import { marked } from "marked";
import DOMPurify from "dompurify";

interface MarkdownProps {
  content: string;
}

export const Markdown = ({ content }: MarkdownProps) => {
  const html = useMemo(() => {
    const raw = marked.parse(content, { breaks: true });
    return DOMPurify.sanitize(raw ?? "");
  }, [content]);

  return <div className="markdown" dangerouslySetInnerHTML={{ __html: html }} />;
};
