import { writable } from "svelte/store";

export const count = writable(0);

setInterval(() => {
  count.update((n) => n + 1);
}, 1000);
