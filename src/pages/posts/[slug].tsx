import { FunctionComponent } from "react";
import { GetStaticProps, GetStaticPaths } from "next";
import ErrorPage from "next/error";
import Head from "next/head";
import { useRouter } from "next/router";

import config from "config";
import Container from "@/components/container";
import PostBody from "@/components/post/body";
import Header from "@/components/post/header";
import PostTitle from "@/components/post/title";
import Layout from "@/components/layout";
import { getPostBySlug, getAllPosts } from "@/lib/posts";
import markdownToHtml from "@/lib/markdownToHtml";
import PostType from "@/types/post";

export const getStaticProps: GetStaticProps = async (context) => {
  const post = getPostBySlug(context.params.slug, ["title", "date", "slug", "content"]);
  const content = await markdownToHtml(post.content || "");

  return {
    props: {
      post: {
        ...post,
        content,
      },
    },
  };
}

export const getStaticPaths: GetStaticPaths = async () => {
  const posts = getAllPosts(["slug"]);

  return {
    paths: posts.map((post) => {
      return {
        params: {
          slug: post.slug,
        },
      };
    }),
    fallback: false,
  };
}

interface PostProps {
  post: PostType;
  morePosts: PostType[];
  preview?: boolean;
}
 
const Post: FunctionComponent<PostProps> = ({ post, morePosts, preview }) => {
  const router = useRouter();
  if (!router.isFallback && !post?.slug) {
    return <ErrorPage statusCode={404} />;
  }
  return (
  <Layout preview={preview}>
    <Container>
      {router.isFallback ? (
        <PostTitle>Loading…</PostTitle>
      ) : (
        <>
          <article className="mb-32">
            <Head>
              <title>
                {post.title} | {config.title}
              </title>
            </Head>
            <Header title={post.title} date={post.date} />
            <PostBody content={post.content} />
          </article>
        </>
      )}
    </Container>
  </Layout>
  );
}
 
export default Post;