import { handleEmployeeManagementRequest } from "./handler.mjs";

export default async function handler(req, res) {
  // Vercel passes req and res, which are Node.js IncomingMessage and ServerResponse
  // Our handler expects the same format, so we can pass them directly
  return handleEmployeeManagementRequest(req, res);
}

