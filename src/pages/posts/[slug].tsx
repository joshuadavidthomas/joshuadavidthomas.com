import fs from "fs";
import matter from "gray-matter";
import { serialize } from "next-mdx-remote/serialize";
import Head from "next/head";
import path from "path";
import Layout from "@/components/layout";
import { postFilePaths, POSTS_PATH } from "@/utils/mdxUtils";
import PostTitle from "@/components/post/title";
import Container from "@/components/container";
import PostBody from "@/components/post/body";
import Header from "@/components/post/header";
import { useRouter } from "next/router";
import config from "config";
import prism from "remark-prism";



// Custom components/renderers to pass to MDX.
// Since the MDX files aren't loaded by webpack, they have no knowledge of how
// to handle import statements. Instead, you must include components in scope
// here.
const components = {
  Head,
};

export default function PostPage({ source, frontMatter }) {
  const router = useRouter();
  
  return (
    <Layout title={frontMatter.title}>
    <Container>
      {router.isFallback ? (
        <PostTitle>Loading…</PostTitle>
      ) : (
        <>
          <article className="mb-32">
            <Head>
              <title>
                {frontMatter.title} | {config.title}
              </title>
            </Head>
            <Header title={frontMatter.title} date={frontMatter.date} />
            <PostBody content={source} components={components} />
          </article>
        </>
      )}
    </Container>
  </Layout>
  );
}

export const getStaticProps = async ({ params }) => {
  const postFilePath = path.join(POSTS_PATH, `${params.slug}.mdx`);
  const source = fs.readFileSync(postFilePath);

  const { content, data } = matter(source);

  const mdxSource = await serialize(content, {
    mdxOptions: {
      remarkPlugins: [prism],
      rehypePlugins: [],
    },
    scope: data,
  });

  return {
    props: {
      source: mdxSource,
      frontMatter: data,
    },
  };
};

export const getStaticPaths = async () => {
  const paths = postFilePaths
    .map((path) => path.replace(/\.mdx?$/, ""))
    .map((slug) => ({ params: { slug } }));

  return {
    paths,
    fallback: false,
  };
};
