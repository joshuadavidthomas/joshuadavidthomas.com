import { FunctionComponent } from 'react';

interface PostBodyProps {
  content: string;
};

const PostBody: FunctionComponent<PostBodyProps> = ({ content }) => (
  <div className="max-w-2xl mx-auto prose dark:prose-invert">
    <div
      dangerouslySetInnerHTML={{ __html: content }}
    />
  </div>
);

export default PostBody;
