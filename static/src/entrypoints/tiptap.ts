import "vite/modulepreload-polyfill";

import { mountSvelteComponents } from "@/utils";
import TipTapEditor from "@/components/TipTapEditor.svelte";

mountSvelteComponents<TipTapEditor>("TipTapEditor", TipTapEditor);
