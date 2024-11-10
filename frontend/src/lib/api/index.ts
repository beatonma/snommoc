import createClient, { Middleware } from "openapi-fetch";
import type { paths } from "./api";

const ApiKey: string = process.env.SNOMMOC_API_KEY!!;

const authMiddleware: Middleware = {
  async onRequest({ request }) {
    request.headers.set("Authorization", ApiKey);
    return request;
  },
};

const client = createClient<paths>({
  baseUrl: "http://localhost:8000/",
});
client.use(authMiddleware);
export default client;
