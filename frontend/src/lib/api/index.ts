import createClient, { Middleware } from "openapi-fetch";
import type { paths } from "./api";
import * as env from "@/env";

const authMiddleware: Middleware = {
  async onRequest({ request }) {
    request.headers.set("Authorization", env.SNOMMOC_API_KEY);
    return request;
  },
};

const client = createClient<paths>({
  baseUrl: process.env.SERVER ?? window.location.origin,
});
client.use(authMiddleware);
export default client;
