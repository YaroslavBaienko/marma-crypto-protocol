/**
 * Marma-Crypto v2.3.0 — Client-Side Forensic Telemetry & Visitor Analytics Agent
 * Captures visitor IP / Geo / ASN, device/browser profile, page views, and granular
 * cryptographic studio actions (Seal Stealth/Visible, Verify, Canary Trace, Downloads).
 * Dispatches events to:
 *   1. Local persistent ring buffer (localStorage["marma_telemetry_events_v23"])
 *   2. Real-time cross-tab BroadcastChannel ("marma_telemetry_live_v23")
 *   3. Optional Marma-Crypto REST API backend (/v2.3/telemetry/ingest)
 */
(function () {
  "use strict";

  const STORAGE_KEY_EVENTS = "marma_telemetry_events_v23";
  const STORAGE_KEY_VISITOR = "marma_visitor_id_v23";
  const STORAGE_KEY_API_URL = "marma_telemetry_api_url_v23";
  const SESSION_KEY_ID = "marma_session_id_v23";
  const SESSION_KEY_GEO = "marma_geo_cache_v23";
  const MAX_LOCAL_EVENTS = 2500;

  const pageLoadTime = Date.now();
  let maxScrollPct = 0;

  function randomHexId(len) {
    const arr = new Uint8Array(Math.ceil(len / 2));
    if (typeof crypto !== "undefined" && crypto.getRandomValues) {
      crypto.getRandomValues(arr);
    } else {
      for (let i = 0; i < arr.length; i++) arr[i] = Math.floor(Math.random() * 256);
    }
    return Array.from(arr, b => b.toString(16).padStart(2, "0")).join("").slice(0, len);
  }

  function safeGetStorage(store, key) {
    try {
      return store ? store.getItem(key) : null;
    } catch (_) {
      return null;
    }
  }

  function safeSetStorage(store, key, val) {
    try {
      if (store) store.setItem(key, val);
    } catch (_) {}
  }

  const locStore = typeof localStorage !== "undefined" ? localStorage : null;
  const sesStore = typeof sessionStorage !== "undefined" ? sessionStorage : null;

  let visitorId = safeGetStorage(locStore, STORAGE_KEY_VISITOR);
  if (!visitorId) {
    visitorId = "vis_" + randomHexId(16);
    safeSetStorage(locStore, STORAGE_KEY_VISITOR, visitorId);
  }

  let sessionId = safeGetStorage(sesStore, SESSION_KEY_ID);
  if (!sessionId) {
    sessionId = "ses_" + randomHexId(12);
    safeSetStorage(sesStore, SESSION_KEY_ID, sessionId);
  }

  const liveChannel = (typeof BroadcastChannel !== "undefined")
    ? new BroadcastChannel("marma_telemetry_live_v23")
    : null;

  function parseUserAgent(uaStr) {
    const ua = String(uaStr || "");
    let browser = "Unknown Browser";
    if (/Edg\/([\d.]+)/.test(ua)) browser = "Edge " + RegExp.$1.split(".")[0];
    else if (/OPR\/([\d.]+)/.test(ua)) browser = "Opera " + RegExp.$1.split(".")[0];
    else if (/Chrome\/([\d.]+)/.test(ua) && !/Chromium/.test(ua)) browser = "Chrome " + RegExp.$1.split(".")[0];
    else if (/Chromium\/([\d.]+)/.test(ua)) browser = "Chromium " + RegExp.$1.split(".")[0];
    else if (/Firefox\/([\d.]+)/.test(ua)) browser = "Firefox " + RegExp.$1.split(".")[0];
    else if (/Version\/([\d.]+).*Safari/.test(ua)) browser = "Safari " + RegExp.$1.split(".")[0];
    else if (/Node\.js/i.test(ua)) browser = "Node.js VM";

    let os = "Unknown OS";
    if (/Windows NT 10\.0/.test(ua)) os = "Windows 10/11";
    else if (/Windows NT/.test(ua)) os = "Windows";
    else if (/Android ([\d.]+)/.test(ua)) os = "Android " + RegExp.$1;
    else if (/iPhone|iPad|iPod/.test(ua)) os = "iOS / iPadOS";
    else if (/Mac OS X ([\d_]+)/.test(ua)) os = "macOS";
    else if (/Debian/i.test(ua)) os = "Debian Linux";
    else if (/Ubuntu/i.test(ua)) os = "Ubuntu Linux";
    else if (/Linux/i.test(ua)) os = "Linux";

    let deviceType = "Desktop";
    if (/Mobi|Android|iPhone|iPod/i.test(ua)) deviceType = "Mobile";
    else if (/iPad|Tablet/i.test(ua)) deviceType = "Tablet";
    else if (/HeadlessChrome/i.test(ua)) deviceType = "Headless / Bot";

    return { browser, os, deviceType };
  }

  const uaProfile = parseUserAgent(typeof navigator !== "undefined" ? navigator.userAgent : "");

  let geoState = {
    ip: "resolving...",
    country: "Unknown",
    country_code: "UN",
    city: "Unknown",
    region: "",
    isp: "Local / Direct",
    asn: "",
    timezone: (typeof Intl !== "undefined" && Intl.DateTimeFormat)
      ? (Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC")
      : "UTC"
  };

  const cachedGeo = safeGetStorage(sesStore, SESSION_KEY_GEO);
  if (cachedGeo) {
    try {
      geoState = Object.assign(geoState, JSON.parse(cachedGeo));
    } catch (_) {}
  }

  async function resolveVisitorIpAndGeo() {
    if (geoState.ip && geoState.ip !== "resolving..." && geoState.ip !== "127.0.0.1") {
      return geoState;
    }
    if (typeof fetch !== "function") {
      geoState.ip = "127.0.0.1";
      return geoState;
    }
    // 1. Primary: ipwho.is (CORS-friendly, no API key required, returns IP + Country + City + ASN/ISP)
    try {
      const ctrl = typeof AbortController !== "undefined" ? new AbortController() : null;
      const timer = ctrl ? setTimeout(() => ctrl.abort(), 3500) : null;
      const r1 = await fetch("https://ipwho.is/", ctrl ? { signal: ctrl.signal } : {});
      if (timer) clearTimeout(timer);
      if (r1 && r1.ok) {
        const d = await r1.json();
        if (d && d.ip) {
          geoState = {
            ip: String(d.ip),
            country: String(d.country || "Unknown"),
            country_code: String(d.country_code || "UN"),
            city: String(d.city || "Unknown"),
            region: String(d.region || ""),
            isp: String((d.connection && (d.connection.isp || d.connection.org)) || "Unknown ISP"),
            asn: (d.connection && d.connection.asn) ? "AS" + d.connection.asn : "",
            timezone: String((d.timezone && d.timezone.id) || geoState.timezone)
          };
          safeSetStorage(sesStore, SESSION_KEY_GEO, JSON.stringify(geoState));
          backfillPendingIpInLocalEvents(geoState);
          return geoState;
        }
      }
    } catch (_) {}

    // 2. Fallback: ipapi.co/json/
    try {
      const ctrl2 = typeof AbortController !== "undefined" ? new AbortController() : null;
      const timer2 = ctrl2 ? setTimeout(() => ctrl2.abort(), 3500) : null;
      const r2 = await fetch("https://ipapi.co/json/", ctrl2 ? { signal: ctrl2.signal } : {});
      if (timer2) clearTimeout(timer2);
      if (r2 && r2.ok) {
        const d2 = await r2.json();
        if (d2 && d2.ip) {
          geoState = {
            ip: String(d2.ip),
            country: String(d2.country_name || "Unknown"),
            country_code: String(d2.country_code || "UN"),
            city: String(d2.city || "Unknown"),
            region: String(d2.region || ""),
            isp: String(d2.org || "Unknown ISP"),
            asn: String(d2.asn || ""),
            timezone: String(d2.timezone || geoState.timezone)
          };
          safeSetStorage(sesStore, SESSION_KEY_GEO, JSON.stringify(geoState));
          backfillPendingIpInLocalEvents(geoState);
          return geoState;
        }
      }
    } catch (_) {}

    // 3. Minimal IP fallback: api.ipify.org
    try {
      const r3 = await fetch("https://api.ipify.org?format=json");
      if (r3 && r3.ok) {
        const d3 = await r3.json();
        if (d3 && d3.ip) {
          geoState.ip = String(d3.ip);
          safeSetStorage(sesStore, SESSION_KEY_GEO, JSON.stringify(geoState));
          backfillPendingIpInLocalEvents(geoState);
          return geoState;
        }
      }
    } catch (_) {}

    if (geoState.ip === "resolving...") {
      geoState.ip = (typeof location !== "undefined" && location.hostname === "localhost") ? "127.0.0.1" : "local-client";
      backfillPendingIpInLocalEvents(geoState);
    }
    return geoState;
  }

  function readLocalEvents() {
    const raw = safeGetStorage(locStore, STORAGE_KEY_EVENTS);
    if (!raw) return [];
    try {
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch (_) {
      return [];
    }
  }

  function writeLocalEvents(events) {
    const trimmed = events.length > MAX_LOCAL_EVENTS
      ? events.slice(events.length - MAX_LOCAL_EVENTS)
      : events;
    safeSetStorage(locStore, STORAGE_KEY_EVENTS, JSON.stringify(trimmed));
  }

  function backfillPendingIpInLocalEvents(resolvedGeo) {
    const events = readLocalEvents();
    let changed = false;
    for (const ev of events) {
      if (ev.session_id === sessionId && (!ev.ip || ev.ip === "resolving..." || ev.ip === "local-client")) {
        ev.ip = resolvedGeo.ip;
        ev.country = resolvedGeo.country;
        ev.country_code = resolvedGeo.country_code;
        ev.city = resolvedGeo.city;
        ev.isp = resolvedGeo.isp;
        ev.asn = resolvedGeo.asn;
        changed = true;
      }
    }
    if (changed) writeLocalEvents(events);
  }

  function getConfiguredApiBaseUrl() {
    const custom = safeGetStorage(locStore, STORAGE_KEY_API_URL);
    if (custom && custom.trim()) return custom.trim().replace(/\/+$/, "");
    if (typeof location !== "undefined" && (location.hostname === "127.0.0.1" || location.hostname === "localhost") && location.port) {
      return `${location.protocol}//${location.host}`;
    }
    return "";
  }

  function sendToBackendApi(eventObj) {
    const baseUrl = getConfiguredApiBaseUrl();
    if (!baseUrl || typeof fetch !== "function") return;
    try {
      fetch(`${baseUrl}/v2.3/telemetry/ingest`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(eventObj),
        keepalive: true
      }).catch(() => {});
    } catch (_) {}
  }

  function detectCurrentPageName() {
    if (typeof location === "undefined") return "index.html";
    const p = location.pathname || "/";
    if (p.endsWith("/ua.html") || p.endsWith("ua.html")) return "ua.html";
    if (p.endsWith("/admin.html") || p.endsWith("admin.html")) return "admin.html";
    return "index.html";
  }

  function track(action, details = {}) {
    const nowIso = new Date().toISOString();
    const ev = {
      event_id: "ev_" + randomHexId(12),
      timestamp: nowIso,
      epoch_ms: Date.now(),
      visitor_id: visitorId,
      session_id: sessionId,
      ip: geoState.ip || "local-client",
      country: geoState.country || "Unknown",
      country_code: geoState.country_code || "UN",
      city: geoState.city || "Unknown",
      region: geoState.region || "",
      isp: geoState.isp || "Local / Direct",
      asn: geoState.asn || "",
      timezone: geoState.timezone || "UTC",
      browser: uaProfile.browser,
      os: uaProfile.os,
      device_type: uaProfile.deviceType,
      user_agent: typeof navigator !== "undefined" ? (navigator.userAgent || "") : "",
      language: typeof navigator !== "undefined" ? (navigator.language || "en") : "en",
      screen: typeof screen !== "undefined" ? `${screen.width || 0}x${screen.height || 0}` : "0x0",
      page: detectCurrentPageName(),
      url: typeof location !== "undefined" ? location.href : "",
      referrer: typeof document !== "undefined" ? (document.referrer || "direct") : "direct",
      action: String(action || "unknown"),
      details: details || {}
    };

    const events = readLocalEvents();
    events.push(ev);
    writeLocalEvents(events);

    if (liveChannel) {
      try {
        liveChannel.postMessage({ type: "marma_telemetry_event", event: ev });
      } catch (_) {}
    }

    sendToBackendApi(ev);
    return ev;
  }

  // Hook into Marma-Crypto interactive functions if present on the page
  function installFunctionHooks() {
    if (typeof window === "undefined") return;

    // 1. Hook sealPdfBytesInBrowser
    if (typeof window.sealPdfBytesInBrowser === "function" && !window.sealPdfBytesInBrowser.__marmaHooked) {
      const origSealPdf = window.sealPdfBytesInBrowser;
      const wrappedSealPdf = function (inputUint8, options = {}) {
        const res = origSealPdf.apply(this, arguments);
        try {
          track("seal_pdf_browser", {
            seal_mode: (res && res.sealPacket && res.sealPacket.seal_mode) || options.sealMode || "stealth",
            signer_name: options.signerName || "Sovereign-Deal-Room-Authority",
            recipient_id: options.recipientId || "(Public)",
            canary_word: (res && res.sealPacket && res.sealPacket.canary && res.sealPacket.canary.beacon_word) || 0,
            bytes: (res && res.sealedBytes && res.sealedBytes.length) || 0,
            content_sha256_prefix: (res && res.sealPacket && (res.sealPacket.content_sha256 || "").slice(0, 16)) || ""
          });
        } catch (_) {}
        return res;
      };
      wrappedSealPdf.__marmaHooked = true;
      window.sealPdfBytesInBrowser = wrappedSealPdf;
    }

    // 2. Hook sealSvgInBrowser
    if (typeof window.sealSvgInBrowser === "function" && !window.sealSvgInBrowser.__marmaHooked) {
      const origSealSvg = window.sealSvgInBrowser;
      const wrappedSealSvg = function (payloadStr, options = {}) {
        const res = origSealSvg.apply(this, arguments);
        try {
          track("seal_svg_browser", {
            signer_name: options.signerName || "Sovereign-Deal-Room-Authority",
            recipient_id: options.recipientId || "(Public)",
            canary_word: (res && res.sealPacket && res.sealPacket.canary && res.sealPacket.canary.beacon_word) || 0,
            bytes: (res && res.sealedBytes && res.sealedBytes.length) || 0
          });
        } catch (_) {}
        return res;
      };
      wrappedSealSvg.__marmaHooked = true;
      window.sealSvgInBrowser = wrappedSealSvg;
    }

    // 3. Hook runOneClickDealRoomDemo
    if (typeof window.runOneClickDealRoomDemo === "function" && !window.runOneClickDealRoomDemo.__marmaHooked) {
      const origDemo = window.runOneClickDealRoomDemo;
      const wrappedDemo = function (mode) {
        try {
          track("dealroom_1click_demo", { mode: mode || "stealth" });
        } catch (_) {}
        return origDemo.apply(this, arguments);
      };
      wrappedDemo.__marmaHooked = true;
      window.runOneClickDealRoomDemo = wrappedDemo;
    }

    // 4. Hook handleFileObject (user drops or selects a file to verify)
    if (typeof window.handleFileObject === "function" && !window.handleFileObject.__marmaHooked) {
      const origHandle = window.handleFileObject;
      const wrappedHandle = async function (file) {
        const res = await origHandle.apply(this, arguments);
        try {
          const banner = document.getElementById("statusBanner");
          const isOk = banner && banner.className && banner.className.includes("ok");
          track("verify_file_drop", {
            file_name: (file && file.name) || "unknown",
            file_size_bytes: (file && file.size) || 0,
            verdict: isOk ? "VERIFIED" : "TAMPER_OR_INVALID"
          });
        } catch (_) {}
        return res;
      };
      wrappedHandle.__marmaHooked = true;
      window.handleFileObject = wrappedHandle;
    }

    // 5. Hook loadRemoteArtifact (preset buttons)
    if (typeof window.loadRemoteArtifact === "function" && !window.loadRemoteArtifact.__marmaHooked) {
      const origLoad = window.loadRemoteArtifact;
      const wrappedLoad = async function (url) {
        try {
          track("verify_preset_load", { artifact_url: String(url || "") });
        } catch (_) {}
        return origLoad.apply(this, arguments);
      };
      wrappedLoad.__marmaHooked = true;
      window.loadRemoteArtifact = wrappedLoad;
    }

    // 6. Hook runCanaryTraceUI
    if (typeof window.runCanaryTraceUI === "function" && !window.runCanaryTraceUI.__marmaHooked) {
      const origTrace = window.runCanaryTraceUI;
      const wrappedTrace = function () {
        const res = origTrace.apply(this, arguments);
        try {
          const inp = document.getElementById("canarySuspectsInput");
          const out = document.getElementById("canaryTraceResult");
          const suspectsRaw = (inp && inp.value) || "";
          const outText = (out && out.textContent) || "";
          track("canary_trace_run", {
            suspects: suspectsRaw.slice(0, 120),
            matched: outText.includes("IDENTIFIED") || outText.includes("ІДЕНТИФІКОВАНО"),
            result_summary: outText.slice(0, 140)
          });
        } catch (_) {}
        return res;
      };
      wrappedTrace.__marmaHooked = true;
      window.runCanaryTraceUI = wrappedTrace;
    }

    // 7. Hook simulateTamperAttack
    if (typeof window.simulateTamperAttack === "function" && !window.simulateTamperAttack.__marmaHooked) {
      const origAttack = window.simulateTamperAttack;
      const wrappedAttack = function () {
        const res = origAttack.apply(this, arguments);
        try {
          const banner = document.getElementById("statusBanner");
          const isTamperedNow = banner && banner.className && banner.className.includes("err");
          track("simulate_tamper_attack", {
            state: isTamperedNow ? "ATTACK_ACTIVE (+0.001 on U2)" : "RESET_TO_CLEAN"
          });
        } catch (_) {}
        return res;
      };
      wrappedAttack.__marmaHooked = true;
      window.simulateTamperAttack = wrappedAttack;
    }

    // 8. Hook toggleLanguage
    if (typeof window.toggleLanguage === "function" && !window.toggleLanguage.__marmaHooked) {
      const origLang = window.toggleLanguage;
      const wrappedLang = function () {
        const res = origLang.apply(this, arguments);
        try {
          track("language_switch", {
            new_lang: (document.documentElement && document.documentElement.lang) || "en"
          });
        } catch (_) {}
        return res;
      };
      wrappedLang.__marmaHooked = true;
      window.toggleLanguage = wrappedLang;
    }

    // 9. Hook downloadSealedCopy
    if (typeof window.downloadSealedCopy === "function" && !window.downloadSealedCopy.__marmaHooked) {
      const origDl = window.downloadSealedCopy;
      const wrappedDl = function (idx) {
        try {
          track("download_sealed_copy", { copy_index: idx });
        } catch (_) {}
        return origDl.apply(this, arguments);
      };
      wrappedDl.__marmaHooked = true;
      window.downloadSealedCopy = wrappedDl;
    }
  }

  function installDomListeners() {
    if (typeof document === "undefined" || !document.addEventListener) return;

    document.addEventListener("click", function (ev) {
      try {
        let el = ev.target;
        while (el && el !== document.body && el.tagName !== "A" && el.tagName !== "BUTTON") {
          el = el.parentElement;
        }
        if (!el) return;
        if (el.tagName === "A") {
          const href = el.getAttribute("href") || "";
          const label = (el.textContent || "").trim().slice(0, 80);
          if (!href || href.startsWith("#")) {
            track("nav_anchor_click", { target: href, label });
          } else {
            track("outbound_link_click", { href, label });
          }
        }
      } catch (_) {}
    }, true);

    if (typeof window !== "undefined" && window.addEventListener) {
      window.addEventListener("scroll", function () {
        try {
          const docEl = document.documentElement;
          const scrollTop = window.scrollY || (docEl && docEl.scrollTop) || 0;
          const scrollHeight = ((docEl && docEl.scrollHeight) || 1) - (window.innerHeight || 0);
          if (scrollHeight > 0) {
            const pct = Math.min(100, Math.round((scrollTop / scrollHeight) * 100));
            if (pct > maxScrollPct) maxScrollPct = pct;
          }
        } catch (_) {}
      }, { passive: true });

      window.addEventListener("pagehide", function () {
        try {
          const durationSec = Math.round((Date.now() - pageLoadTime) / 1000);
          track("session_exit", {
            duration_sec: durationSec,
            max_scroll_pct: maxScrollPct
          });
        } catch (_) {}
      });
    }
  }

  // Expose public API for admin panel and tests
  if (typeof window !== "undefined") {
    window.MarmaTelemetry = {
      track,
      readLocalEvents,
      writeLocalEvents,
      resolveVisitorIpAndGeo,
      getGeoState: () => Object.assign({}, geoState),
      getSessionId: () => sessionId,
      getVisitorId: () => visitorId,
      getConfiguredApiBaseUrl,
      setConfiguredApiBaseUrl: (url) => safeSetStorage(locStore, STORAGE_KEY_API_URL, String(url || "").trim()),
      STORAGE_KEY_EVENTS
    };
  }

  // Auto-initialize on page load (skip auto page_view on admin.html itself to keep visitor stats clean)
  try {
    installFunctionHooks();
    installDomListeners();
    const pageName = detectCurrentPageName();
    if (pageName !== "admin.html") {
      track("page_view", {
        page: pageName,
        title: typeof document !== "undefined" ? (document.title || "").slice(0, 100) : ""
      });
      resolveVisitorIpAndGeo();
    }
  } catch (_) {}
})();
