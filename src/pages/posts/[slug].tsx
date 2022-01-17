import fs from "fs";
import matter from "gray-matter";
import { MDXRemote } from "next-mdx-remote";
import { serialize } from "next-mdx-remote/serialize";
import Head from "next/head";
import path from "path";
import Layout from "@/components/layout";
import { postFilePaths, POSTS_PATH } from "@/utils/mdxUtils";
import DateFormatter from "@/components/date-formatter";
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

export default function PostPage({ source, frontMatter, siteTitle }) {
  const router = useRouter();

  return (
    <Layout title={frontMatter.title}>
        {router.isFallback ? (
          <div>Loading…</div>
        ) : (
          <>
            <Head>
              <title>
                {frontMatter.title} | {siteTitle}
              </title>
            </Head>
            <article className="max-w-2xl px-2 mx-auto mb-32">
              <header>
                <h1 className="mb-12 text-3xl font-bold leading-tight tracking-tighter md:text-3xl lg:text-4xl">
                  {frontMatter.title}
                </h1>
                <section>
                  <div className="mb-6 text-lg">
                    <DateFormatter dateStr={frontMatter.date} />
                  </div>
                </section>
              </header>
              <section className="mx-auto prose dark:prose-invert">
                <MDXRemote {...source} components={components} />
              </section>
            </article>
          </>
        )}
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
      siteTitle: config.title,
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
