import { FunctionComponent } from "react";
import Image from "next/image";

import Layout from "@/components/layout";
import PostPreview from "@/components/post/preview";
import { getAllPosts } from "@/lib/posts";
import Post from "@/types/post";

interface IndexProps {
  allPosts: Post[];
}

export const getStaticProps = async () => {
  const allPosts = getAllPosts(["title", "date", "slug", "excerpt"]);
  return {
    props: { allPosts },
  };
};

const Index: FunctionComponent<IndexProps> = ({ allPosts }) => {
  return (
    <>
      <Layout title="Joshua David Thomas">
        <div className="container max-w-2xl mx-auto">
          <section className="pb-10 mx-auto sm:pt-10 sm:pb-40">
            <div className="flex items-center justify-center py-10">
              <Image
                src="/me.png"
                width="250"
                height="250"
                alt="A picture of Josh"
                className="rounded-full shadow-md"
              />
            </div>
            <h1 className="text-5xl leading-relaxed">
              👋
              <span className="pl-2 font-bold tracking-wide">
                Hi, my name is Josh.
              </span>
            </h1>
            <p className="text-2xl font-medium leading-9">
              I am a web developer in Tuscaloosa, AL.
            </p>
            <div className="pt-4 space-y-1">
              <p>I use Python and Django to make things on the web.</p>
              <p>
                If you want, you can say{" "}
                <a
                  className="hover:text-[#050]"
                  href="mailto:hello@joshuadavidthomas.com"
                >
                  hello
                </a>
                .
              </p>
            </div>
          </section>
          <section>
            <h2 className="mb-8 text-2xl font-bold leading-tight tracking-tight">
              Latest Posts
            </h2>
            <div className="space-y-12">
              {allPosts.map((post) => (
                <PostPreview
                  key={post.slug}
                  title={post.title}
                  date={post.date}
                  slug={post.slug}
                  excerpt={post.excerpt}
                />
              ))}
            </div>
          </section>
        </div>
      </Layout>
    </>
  );
};

export default Index;
