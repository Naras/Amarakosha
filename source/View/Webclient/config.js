// Configuration constants for Amarakosha API connection
let API_BASE_URL = "http://127.0.0.1:5002/Amarakosha/api/v1.0";

// Automatically detect Lightsail server based on browser URL
if (window.location.hostname === "app.iyengarlabs.org" || window.location.host.includes("iyengarlabs.org")) {
  API_BASE_URL = "https://app.iyengarlabs.org/amarakosha-rest-api";
}

// Deprecated: kept temporarily for backward compatibility if referenced directly
const API_URL = "127.0.0.1";
const API_PORT = "5002";
const API_PREFIX = "/Amarakosha/api/v1.0/";

function getScriptParam() {
  const script = sessionStorage.getItem("script");
  if (!script || script === "null" || script === "undefined") {
    return "";
  }
  return script;
}

function getApiUrl(endpoint) {
  const base = API_BASE_URL.replace(/\/+$/, "");
  const cleanEndpoint = endpoint.replace(/^\/+/, "");
  let fullUrl = `${base}/${cleanEndpoint}`;
  
  const script = getScriptParam();
  if (script) {
    fullUrl += fullUrl.includes("?") ? `&script=${script}` : `?script=${script}`;
  }
  return fullUrl;
}
