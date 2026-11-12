// Builds dist/stats.svg: a GitHub stats card in the same style as the rest of the profile.
// Run in CI with GITHUB_TOKEN + LOGIN set. Run locally with --mock to render sample data.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";

const LOGIN = process.env.LOGIN || "gavenrobertson";
const MOCK = process.argv.includes("--mock");
const OUT = process.argv.includes("--out") ? process.argv[process.argv.indexOf("--out") + 1] : "dist/stats.svg";

const C = {
  bg: "#0C1611", panel: "#12211A", line: "#1F3529", dim: "#5E7A68", mid: "#93AE9C",
  text: "#F4EFD8", accent: "#FEE123", green: "#4CD07D", red: "#FF6B5E",
};
const MONO = "font-family:JB, ui-monospace, Menlo, Consolas, monospace";
const SANS = "font-family:BG, 'Segoe UI', Helvetica, Arial, sans-serif";

const QUERY = `query($login:String!){
  user(login:$login){
    followers{ totalCount }
    repositories(first:100, ownerAffiliations:OWNER, isFork:false, orderBy:{field:STARGAZERS, direction:DESC}){
      totalCount
      nodes{ stargazerCount languages(first:10, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{ name color } } } }
    }
    contributionsCollection{
      totalCommitContributions
      restrictedContributionsCount
      totalPullRequestContributions
      totalPullRequestReviewContributions
      totalIssueContributions
      contributionCalendar{ totalContributions }
    }
  }
}`;

async function fetchData() {
  if (MOCK) {
    return {
      followers: { totalCount: 42 },
      repositories: {
        totalCount: 18,
        nodes: [
          { stargazerCount: 31, languages: { edges: [
            { size: 90000, node: { name: "TypeScript", color: "#3178c6" } },
            { size: 20000, node: { name: "CSS", color: "#663399" } } ] } },
          { stargazerCount: 12, languages: { edges: [
            { size: 140000, node: { name: "C++", color: "#f34b7d" } },
            { size: 30000, node: { name: "CMake", color: "#DA3434" } } ] } },
          { stargazerCount: 5, languages: { edges: [
            { size: 50000, node: { name: "Rust", color: "#dea584" } },
            { size: 40000, node: { name: "TypeScript", color: "#3178c6" } },
            { size: 12000, node: { name: "Python", color: "#3572A5" } } ] } },
        ],
      },
      contributionsCollection: {
        totalCommitContributions: 612, restrictedContributionsCount: 240,
        totalPullRequestContributions: 38, totalPullRequestReviewContributions: 11,
        totalIssueContributions: 9, contributionCalendar: { totalContributions: 910 },
      },
    };
  }
  const token = process.env.GITHUB_TOKEN;
  if (!token) throw new Error("GITHUB_TOKEN is required (or pass --mock)");
  const res = await fetch("https://api.github.com/graphql", {
    method: "POST",
    headers: { authorization: `bearer ${token}`, "content-type": "application/json", "user-agent": "profile-stats" },
    body: JSON.stringify({ query: QUERY, variables: { login: LOGIN } }),
  });
  if (!res.ok) throw new Error(`GraphQL HTTP ${res.status}: ${await res.text()}`);
  const json = await res.json();
  if (json.errors) throw new Error("GraphQL errors: " + JSON.stringify(json.errors));
  return json.data.user;
}

const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const fmt = (n) => n >= 10000 ? (n / 1000).toFixed(1).replace(/\.0$/, "") + "k" : String(n);

function fontFaces() {
  // Reuse the fonts already embedded in the header so the card matches exactly.
  const header = readFileSync(new URL("../assets/header.svg", import.meta.url), "utf8");
  const m = header.match(/<style>([\s\S]*?)<\/style>/);
  const faces = (m ? m[1] : "").match(/@font-face\{[^}]*\}/g) || [];
  return faces.join("");
}

function build(u) {
  const cc = u.contributionsCollection;
  const commits = cc.totalCommitContributions + cc.restrictedContributionsCount;
  const stars = u.repositories.nodes.reduce((a, r) => a + r.stargazerCount, 0);
  const year = new Date().getUTCFullYear();

  // Languages weighted by bytes across non-fork repos.
  const langs = new Map();
  for (const r of u.repositories.nodes)
    for (const e of r.languages.edges) {
      const cur = langs.get(e.node.name) || { size: 0, color: e.node.color || C.mid };
      cur.size += e.size; langs.set(e.node.name, cur);
    }
  const total = [...langs.values()].reduce((a, l) => a + l.size, 0) || 1;
  const top = [...langs.entries()].sort((a, b) => b[1].size - a[1].size).slice(0, 6)
    .map(([name, l]) => ({ name, color: l.color, pct: (l.size / total) * 100 }));

  const W = 990, H = 390;
  const tiles = [
    { label: `contributions · ${year}`, value: fmt(cc.contributionCalendar.totalContributions), color: C.accent },
    { label: "commits", value: fmt(commits), color: C.text },
    { label: "pull requests", value: fmt(cc.totalPullRequestContributions), color: C.text },
    { label: "reviews + issues", value: fmt(cc.totalPullRequestReviewContributions + cc.totalIssueContributions), color: C.text },
    { label: "stars earned", value: fmt(stars), color: C.accent },
    { label: "followers", value: fmt(u.followers.totalCount), color: C.text },
  ];

  let s = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="GitHub stats for ${esc(LOGIN)}">`;
  s += `<title>GitHub stats for ${esc(LOGIN)}: ${tiles.map(t => `${t.value} ${t.label}`).join(", ")}</title>`;
  s += `<style>${fontFaces()}`;
  s += `.cur{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}`;
  s += `.bar{transform-origin:left center;animation:grow 1.4s cubic-bezier(.2,.8,.2,1) both}@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}`;
  s += `.num{animation:rise .9s cubic-bezier(.2,.8,.2,1) both}@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}`;
  s += `@media (prefers-reduced-motion:reduce){.cur,.bar,.num{animation:none}}</style>`;
  s += `<rect width="${W}" height="${H}" rx="22" fill="${C.bg}"/>`;
  s += `<rect x="1" y="1" width="${W - 2}" height="${H - 2}" rx="21" fill="none" stroke="${C.line}" stroke-width="2"/>`;
  // title bar
  s += `<path d="M2 62 H${W - 2}" stroke="${C.line}" stroke-width="2"/>`;
  s += `<circle cx="34" cy="32" r="6" fill="${C.red}" opacity=".85"/><circle cx="54" cy="32" r="6" fill="${C.accent}" opacity=".85"/><circle cx="74" cy="32" r="6" fill="${C.green}" opacity=".85"/>`;
  s += `<text x="100" y="38" style="${MONO};font-size:17px" fill="${C.mid}"><tspan fill="${C.accent}" font-weight="700">~</tspan> $ gh stats <tspan fill="${C.text}">@${esc(LOGIN)}</tspan><tspan class="cur" fill="${C.accent}">_</tspan></text>`;
  const stamp = new Date().toISOString().slice(0, 10);
  s += `<text x="${W - 30}" y="38" text-anchor="end" style="${MONO};font-size:14px" fill="${C.dim}">updated ${stamp}</text>`;

  // metric tiles, 3 x 2 on the left
  const gx = 30, gy = 88, tw = 180, th = 128, gap = 14;
  tiles.forEach((t, i) => {
    const x = gx + (i % 3) * (tw + gap), y = gy + Math.floor(i / 3) * (th + gap);
    s += `<rect x="${x}" y="${y}" width="${tw}" height="${th}" rx="16" fill="${C.panel}" stroke="${C.line}" stroke-width="1.5"/>`;
    s += `<text class="num" style="${SANS};font-weight:800;font-size:44px;letter-spacing:-1px;animation-delay:${(i * 0.08).toFixed(2)}s" x="${x + 20}" y="${y + 66}" fill="${t.color}">${esc(t.value)}</text>`;
    s += `<text style="${MONO};font-size:14px" x="${x + 20}" y="${y + 100}" fill="${C.dim}">${esc(t.label)}</text>`;
  });

  // languages on the right
  const lx = gx + 3 * tw + 2 * gap + 30, ly = gy, lw = W - lx - 30;
  s += `<text x="${lx}" y="${ly + 18}" style="${MONO};font-size:15px" fill="${C.dim}"><tspan fill="${C.accent}">#</tspan> top languages</text>`;
  // stacked bar
  const bx = lx, by = ly + 36, bw = lw, bh = 14;
  s += `<clipPath id="barclip"><rect x="${bx}" y="${by}" width="${bw}" height="${bh}" rx="7"/></clipPath>`;
  s += `<rect x="${bx}" y="${by}" width="${bw}" height="${bh}" rx="7" fill="${C.panel}"/>`;
  let acc = 0;
  top.forEach((l, i) => {
    const w = Math.max(2, (l.pct / 100) * bw);
    s += `<rect class="bar" style="animation-delay:${(0.1 + i * 0.1).toFixed(2)}s" clip-path="url(#barclip)" x="${(bx + acc).toFixed(1)}" y="${by}" width="${w.toFixed(1)}" height="${bh}" fill="${l.color}"/>`;
    acc += w;
  });
  // legend rows
  top.forEach((l, i) => {
    const y = by + 46 + i * 34;
    s += `<circle cx="${lx + 8}" cy="${y - 5}" r="6" fill="${l.color}"/>`;
    s += `<text x="${lx + 24}" y="${y}" style="${MONO};font-size:16px" fill="${C.text}">${esc(l.name)}</text>`;
    s += `<text x="${lx + lw}" y="${y}" text-anchor="end" style="${MONO};font-size:15px" fill="${C.mid}">${l.pct.toFixed(1)}%</text>`;
  });
  if (top.length === 0)
    s += `<text x="${lx}" y="${by + 46}" style="${MONO};font-size:15px" fill="${C.dim}">no language data yet</text>`;

  s += `</svg>`;
  return s;
}

const user = await fetchData();
const svg = build(user);
mkdirSync(OUT.replace(/\/[^/]*$/, "") || ".", { recursive: true });
writeFileSync(OUT, svg);
console.log(`wrote ${OUT} (${svg.length} bytes)`);
