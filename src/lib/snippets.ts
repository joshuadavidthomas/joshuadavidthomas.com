import fs from "fs";
import path from "path";
import matter from "gray-matter";
import { CONTENT_PATH, getSubDirs, stripMDXExtension } from './mdx';

export const SNIPPETS_PATH = path.join(CONTENT_PATH, "snippets");

export const getSnippetCategories = (): string[] => {
  return getSubDirs(SNIPPETS_PATH);
};

export const getSnippetSlugs = (category: string) => {
  const categoryPath = path.join(SNIPPETS_PATH, category);
  const snippets = fs.readdirSync(categoryPath);
  const slugs = snippets.map((slug) => {
    return stripMDXExtension(slug);
  });
  return slugs;
};

export const getSnippetByCategoryAndSlug = (category: string, slug: string, fields: string[] = []) => {
  const categoryPath = path.join(SNIPPETS_PATH, category);
  const fullPath = path.join(categoryPath, `${slug}.mdx`);
  const fileContents = fs.readFileSync(fullPath, "utf8");
  const { data, content } = matter(fileContents);

  type Items = {
    [key: string]: string;
  };

  const items: Items = {};

  fields.forEach((field) => {
    if (field === "slug") {
      items[field] = slug;
    }
    if (field === "content") {
      items[field] = content;
    }
    if (field === "category") {
      items[field] = category;
    }
    if (typeof data[field] !== "undefined") {
      items[field] = data[field];
    }
  });

  return items;
};

export const getAllSnippetsByCategory = (fields: string[] = []) => {
  const categories = getSnippetCategories();
  const snippets = categories.map((category) => {
    const slugs = getSnippetSlugs(category);
    const snippet = slugs.map((slug) => {
      return getSnippetByCategoryAndSlug(category, slug, fields);
    });
    return {
      category,
      snippets: snippet,
    }
  });
  return snippets.flat();
}

export const getAllSnippets = (fields: string[] = []) => {
  const categories = getSnippetCategories();
  const snippets = categories.map((category) => {
    const slugs = getSnippetSlugs(category);
    const snippet = slugs.map((slug) => {
      return getSnippetByCategoryAndSlug(category, slug, fields);
    });
    return snippet;
  });
  return snippets.flat();
}