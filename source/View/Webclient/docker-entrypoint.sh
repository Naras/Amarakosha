#!/bin/sh
if [ -n "$API_URL" ]; then
  cat <<EOF > /usr/share/nginx/html/config.js
let API_BASE_URL = "$API_URL";

if (window.location.hostname === "app.iyengarlabs.org" || window.location.host.includes("iyengarlabs.org")) {
  API_BASE_URL = "https://app.iyengarlabs.org/amarakosha-rest-api";
}

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
  let fullUrl = \`\${base}/\${cleanEndpoint}\`;
  
  const script = getScriptParam();
  if (script) {
    fullUrl += fullUrl.includes("?") ? \`&script=\${script}\` : \`?script=\${script}\`;
  }
  return fullUrl;
}
EOF
fi

exec nginx -g "daemon off;"
