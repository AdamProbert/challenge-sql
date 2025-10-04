import axios from "axios";

const fallbackBaseURL = "/api";
const baseURL = import.meta.env.VITE_API_BASE_URL ?? fallbackBaseURL;

export const apiClient = axios.create({
  baseURL,
  timeout: 5000,
});
