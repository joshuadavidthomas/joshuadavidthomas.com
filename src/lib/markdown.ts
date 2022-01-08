import ReactMarkdown from "react-markdown";

export const markdownToHtml = async (markdown: string) => {
  return <ReactMarkdown>{markdown}</ReactMarkdown>;
};

export default markdownToHtml;
