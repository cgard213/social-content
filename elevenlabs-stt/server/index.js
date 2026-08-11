#!/usr/bin/env node
/**
 * Minimal MCP stdio server exposing one tool: transcribe_audio.
 *
 * Hand-rolled JSON-RPC rather than the MCP SDK so the bundle has zero dependencies and
 * no npm install step. Claude Desktop ships its own Node, so this runs as-is.
 *
 * The reason this exists at all: Cowork works inside a Linux VM whose network allowlist
 * covers Anthropic, pypi and npm and nothing else, so it cannot call ElevenLabs itself.
 * This server runs out on the host, where there is normal internet, and reads the file
 * through the same folder the VM has mounted.
 *
 * That mount is also why path resolution below is more forgiving than it looks. The path
 * the model sees inside the VM is not the path this process sees on the host, so a plain
 * "file not found" would be the normal case rather than the exception.
 */

const fs = require("fs");
const path = require("path");

const API_KEY = process.env.ELEVENLABS_API_KEY || "";
const MEDIA_ROOT = process.env.MEDIA_ROOT || "";
const MODEL_ID = process.env.ELEVENLABS_MODEL_ID || "scribe_v2";
const ENDPOINT = "https://api.elevenlabs.io/v1/speech-to-text";

const TOOL = {
  name: "transcribe_audio",
  description:
    "Transcribe an audio or video file with ElevenLabs Scribe and write word-level " +
    "timings to JSON. Returns a summary and the path of the file it wrote. Pass the " +
    "small extracted wav rather than the original video when you have one.",
  inputSchema: {
    type: "object",
    properties: {
      file_path: {
        type: "string",
        description:
          "Path to the audio or video file. A path relative to the working folder is " +
          "safest, for example work/audio.wav",
      },
      output_path: {
        type: "string",
        description: "Where to write the JSON. Defaults to work/words.json",
      },
    },
    required: ["file_path"],
  },
};

/* ---------- path resolution across the VM / host boundary ---------- */

function findByName(dir, name, depth) {
  if (depth < 0) return null;
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return null;
  }
  for (const e of entries) {
    if (e.isFile() && e.name === name) return path.join(dir, e.name);
  }
  for (const e of entries) {
    if (e.isDirectory() && !e.name.startsWith(".") && e.name !== "node_modules") {
      const hit = findByName(path.join(dir, e.name), name, depth - 1);
      if (hit) return hit;
    }
  }
  return null;
}

function resolveInput(given) {
  const tries = [given];
  if (MEDIA_ROOT) {
    tries.push(path.join(MEDIA_ROOT, given));
    tries.push(path.join(MEDIA_ROOT, given.replace(/^[/\\]+/, "")));
  }
  for (const t of tries) {
    try {
      if (fs.statSync(t).isFile()) return t;
    } catch {
      /* keep looking */
    }
  }
  // Last resort: the model gave us a VM path. Match on the filename instead.
  if (MEDIA_ROOT) {
    const hit = findByName(MEDIA_ROOT, path.basename(given), 4);
    if (hit) return hit;
  }
  return null;
}

function resolveOutput(given, inputFile) {
  if (!given) {
    const base = MEDIA_ROOT || path.dirname(inputFile);
    return path.join(base, "work", "words.json");
  }
  if (path.isAbsolute(given) && fs.existsSync(path.dirname(given))) return given;
  if (MEDIA_ROOT) return path.join(MEDIA_ROOT, given.replace(/^[/\\]+/, ""));
  return path.resolve(given);
}

/* ---------- the tool ---------- */

async function transcribe({ file_path, output_path }) {
  if (!API_KEY) {
    return err(
      "No ElevenLabs API key configured. Open Claude Desktop settings, find this " +
        "extension, and paste your key."
    );
  }

  const input = resolveInput(file_path);
  if (!input) {
    return err(
      `Could not find ${file_path}. Looked at that path directly and searched under ` +
        `${MEDIA_ROOT || "(no working folder configured)"}. If the working folder is ` +
        `wrong, fix it in this extension's settings.`
    );
  }

  const buf = fs.readFileSync(input);
  const form = new FormData();
  form.append("file", new Blob([buf]), path.basename(input));
  form.append("model_id", MODEL_ID);

  let res;
  try {
    // xi-api-key ONLY. Sending Authorization as well is a hard 401 with
    // "Only one of xi-api-key and authorization headers must be provided", which
    // reads like a bad key and is not one.
    res = await fetch(ENDPOINT, {
      method: "POST",
      headers: { "xi-api-key": API_KEY },
      body: form,
    });
  } catch (e) {
    return err(`Could not reach ElevenLabs: ${e.message}`);
  }

  if (!res.ok) {
    const body = await res.text().catch(() => "");
    let detail = "";
    try {
      const parsed = JSON.parse(body);
      detail = parsed?.detail?.message || parsed?.detail?.status || "";
    } catch {
      detail = body.slice(0, 300);
    }
    if (res.status === 401) {
      return err(
        `ElevenLabs refused the request: ${detail || "unauthorized"}\n\n` +
          "If it mentions a missing permission, the key is real but scoped too " +
          "narrowly. Make a new key with speech to text enabled."
      );
    }
    if (res.status === 429) {
      return err(
        "Out of ElevenLabs credits for this month. Switch to the local model, or " +
          "wait for the monthly reset."
      );
    }
    return err(`ElevenLabs returned ${res.status}. ${detail}`);
  }

  const data = await res.json();
  const words = (data.words || [])
    .filter((w) => w.type === "word" || w.type === undefined)
    .filter((w) => w.text && w.text.trim())
    .map((w) => ({
      text: w.text.trim(),
      start: round(w.start),
      end: round(w.end),
    }));

  const out = resolveOutput(output_path, input);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(
    out,
    JSON.stringify(
      { text: data.text || "", words, source: "elevenlabs", model: MODEL_ID },
      null,
      1
    )
  );

  const rel = MEDIA_ROOT ? path.relative(MEDIA_ROOT, out) : out;
  const last = words.length ? words[words.length - 1].end : 0;
  const preview = words.slice(0, 30).map((w) => w.text).join(" ");

  return ok(
    `Transcribed ${path.basename(input)}: ${words.length} words over ${last.toFixed(1)}s.\n` +
      `Written to ${rel}\n\nOpening words: ${preview}${words.length > 30 ? " ..." : ""}`
  );
}

const round = (n) => (typeof n === "number" ? Math.round(n * 1000) / 1000 : 0);
const ok = (text) => ({ content: [{ type: "text", text }] });
const err = (text) => ({ content: [{ type: "text", text }], isError: true });

/* ---------- JSON-RPC over stdio ---------- */

function send(msg) {
  process.stdout.write(JSON.stringify(msg) + "\n");
}

// Requests still awaiting a response. A transcription takes seconds, and if stdin
// closes while one is in flight we must finish it rather than exit mid-call.
let inFlight = 0;
let stdinClosed = false;

function maybeExit() {
  if (stdinClosed && inFlight === 0) process.exit(0);
}

async function handle(msg) {
  const { id, method, params } = msg;
  if (id === undefined) return; // notification, nothing to answer

  switch (method) {
    case "initialize":
      return send({
        jsonrpc: "2.0",
        id,
        result: {
          protocolVersion: (params && params.protocolVersion) || "2025-06-18",
          capabilities: { tools: {} },
          serverInfo: { name: "elevenlabs-stt", version: "1.0.0" },
        },
      });

    case "ping":
      return send({ jsonrpc: "2.0", id, result: {} });

    case "tools/list":
      return send({ jsonrpc: "2.0", id, result: { tools: [TOOL] } });

    case "tools/call": {
      const name = params && params.name;
      if (name !== TOOL.name) {
        return send({
          jsonrpc: "2.0",
          id,
          error: { code: -32602, message: `Unknown tool: ${name}` },
        });
      }
      inFlight++;
      try {
        const result = await transcribe((params && params.arguments) || {});
        send({ jsonrpc: "2.0", id, result });
      } catch (e) {
        send({ jsonrpc: "2.0", id, result: err(`Failed: ${e.message}`) });
      } finally {
        inFlight--;
        maybeExit();
      }
      return;
    }

    default:
      return send({
        jsonrpc: "2.0",
        id,
        error: { code: -32601, message: `Method not found: ${method}` },
      });
  }
}

let buffer = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => {
  buffer += chunk;
  let nl;
  while ((nl = buffer.indexOf("\n")) !== -1) {
    const line = buffer.slice(0, nl).trim();
    buffer = buffer.slice(nl + 1);
    if (!line) continue;
    try {
      handle(JSON.parse(line));
    } catch {
      /* ignore anything that is not a message */
    }
  }
});
process.stdin.on("end", () => {
  stdinClosed = true;
  maybeExit();
});
