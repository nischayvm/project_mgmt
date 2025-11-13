import { handleEmployeeManagementRequest } from "./handler.mjs";

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(request, response) {
  return handleEmployeeManagementRequest(request, response);
}

