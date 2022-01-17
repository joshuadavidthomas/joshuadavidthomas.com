import { FunctionComponent, useEffect } from "react";
import { GetStaticPaths, GetStaticProps } from "next";
import Head from "next/head";
import { MDXRemote, MDXRemoteSerializeResult } from "next-mdx-remote";
import path from "path";

import config from "config";
import Layout from "@/components/layout";
import {
  getSnippetCategories,
  getSnippetSlugs,
  SNIPPETS_PATH,
} from "@/lib/snippets";
import { processRawFile, mdxToHTML } from "@/lib/mdx";

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const snippetFilePath = path.join(
    SNIPPETS_PATH,
    `${params.category}/${params.slug}.mdx`
  );
  const { content, data } = processRawFile(snippetFilePath);
  const mdxSource = await mdxToHTML(content, data);

  return {
    props: {
      source: mdxSource,
      frontMatter: data,
    },
  };
};

export const getStaticPaths: GetStaticPaths = async () => {
  const categories = getSnippetCategories();
  const paths = categories.map((category) => {
    const snippets = getSnippetSlugs(category);
    return snippets.map((snippet) => ({
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
}

const Snippet: FunctionComponent<SnippetProps> = ({ source, frontMatter }) => {
  if (!frontMatter || !source) {
    return null;
  }
  const { title, description, date, updated } = frontMatter;

  return (
    <Layout title={title} description={description}>
      <Head>
        <title>{title} | {config.title}</title>
        <meta name="description" content={description} />
      </Head>
      <div className="mx-auto prose dark:prose-invert">
        <h1>{title}</h1>
        <p>
          Published:
          <time className="pl-2">{date}</time>
        </p>
        {updated && (
          <p>
            Updated:
            <time className="pl-2">{updated}</time>
          </p>
        )}
        <MDXRemote {...source} />
      </div>
    </Layout>
  );
};

export default Snippet;
