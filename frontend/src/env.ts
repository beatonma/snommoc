const SERVER = process.env.SERVER!;
export const SNOMMOC_API_KEY = process.env.SNOMMOC_API_KEY!;

export const resolveUrl = (path: string) => new URL(path, SERVER).href;
