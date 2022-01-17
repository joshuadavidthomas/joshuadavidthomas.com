import { FunctionComponent } from 'react';
import { MDXRemote } from "next-mdx-remote";

interface PostBodyProps {
  content: any;
  components: any;
};

const PostBody: FunctionComponent<PostBodyProps> = ({ content, components }) => (
  <div className="max-w-2xl mx-auto prose dark:prose-invert">
    <MDXRemote {...content} components={components} />
  </div>
);

export default PostBody;
