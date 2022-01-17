import { FunctionComponent } from "react";
import { GetStaticPaths, GetStaticProps } from 'next';
import Head from "next/head";
import { useRouter } from "next/router";
import { MDXRemote } from "next-mdx-remote";
import path from "path";
import config from "config";
import type { MDXRemoteSerializeResult } from "next-mdx-remote";
import Layout from "@/components/layout";
import { getSnippetCategories, getSnippetSlugs } from "@/lib/snippets";
import { SNIPPETS_PATH } from "@/lib/snippets";
import { processRawFile, mdxToHTML } from "@/lib/mdx";

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const snippetFilePath = path.join(SNIPPETS_PATH, `${params.category}/${params.slug}.mdx`);
  const { content, data } = processRawFile(snippetFilePath);
  const mdxSource = await mdxToHTML(content, data);

  return {
    props: {
      source: mdxSource,
      frontMatter: data,
      siteTitle: config.title,
    },
  };
};

export const getStaticPaths: GetStaticPaths = async () => {
  const categories = getSnippetCategories();
  const paths = categories.map(category => {
    const snippets = getSnippetSlugs(category);
    return snippets.map(snippet => ({
      params: {
        category,
        slug: snippet,
      },
    }));
  });

  return {
    paths: paths.flat(),
    fallback: true,
  };
};

interface SnippetProps {
  source: MDXRemoteSerializeResult;
  frontMatter: any;
  siteTitle: string;
}
 
const Snippet: FunctionComponent<SnippetProps> = ({ source, frontMatter, siteTitle }) => {
  return (
      <Layout title={frontMatter.title} description={frontMatter.description}>
      <Head>
        <title>{frontMatter.title} | {config.title}</title>
        <meta name="description" content={frontMatter.description} />
      </Head>
      <div className="mx-auto prose dark:prose-invert">
      <MDXRemote {...source} />
      </div>
      </Layout>
  );
}
 
export default Snippet;