import fs from "fs";
import path from "path";
import matter from "gray-matter";
import { serialize } from "next-mdx-remote/serialize";
import prism from "remark-prism";

export const CONTENT_PATH = path.join(process.cwd(), "content");

export const getSubDirs = (dir: string): string[] => {
  return fs.readdirSync(dir).filter((subDir) => {
    const isDirectory = fs.statSync(path.join(dir, subDir)).isDirectory();
    return isDirectory;
  });
};

export const stripMDXExtension = (filePath: string): string => {
  return filePath.replace(/\.mdx$/, "");
};

export const processRawFile = (filePath: string) => {
  const source = fs.readFileSync(filePath, "utf8");
  return matter(source);
};

export const mdxToHTML = async (content, data) => {
  return await serialize(content, {
    mdxOptions: {
      remarkPlugins: [prism],
      rehypePlugins: [],
    },
    scope: data,
  });
};