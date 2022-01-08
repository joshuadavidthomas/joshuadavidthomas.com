import { FunctionComponent } from "react";
import Link from "next/link";
import DateFormatter from "../date-formatter";

interface PreviewProps {
  title: string;
  date: string;
  excerpt: string;
  slug: string;
}

const Preview: FunctionComponent<PreviewProps> = ({
  title,
  date,
  excerpt,
  slug,
}) => {
  return (
    <div>
      <h3 className="mb-3 text-xl font-medium leading-snug">
        <Link as={`/posts/${slug}`} href="/posts/[slug]">
          <a className="hover:underline">{title}</a>
        </Link>
      </h3>
      <div className="mb-4">
        <DateFormatter dateStr={date} />
      </div>
      <p className="mb-4 leading-relaxed">{excerpt}</p>
    </div>
  );
};

export default Preview;
