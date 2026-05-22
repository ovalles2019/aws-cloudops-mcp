const $ = (sel) => document.querySelector(sel);

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function showErr(msg) {
  const e = $("err-banner");
  if (!e) return;
  e.textContent = msg || "";
  e.style.display = msg ? "block" : "none";
}

function stateClass(s) {
  const k = (s || "").replace(/\s+/g, "-");
  return `state state-${k}`;
}

function applyDemoMode(demo) {
  const banner = $("demo-banner");
  if (banner) banner.style.display = demo ? "block" : "none";
  if (demo) {
    setText("eyebrow", "Portfolio demo");
    setText("tagline", "Synthetic AWS inventory — real MCP tools use your credentials in Cursor.");
  }
}

function render(d) {
  applyDemoMode(!!d.demo_mode);
  const w = d.whoami || {};
  setText("id-account", w.account || "—");
  setText("id-region", w.region || "—");
  setText("id-arn", w.arn || "—");

  const s = d.summary || {};
  setText("m-ec2", `${s.ec2_running ?? "—"}/${s.ec2_total ?? "—"}`);
  setText("m-alarms", String(s.alarms_in_alarm ?? "—"));
  setText("m-alb", String(s.load_balancers ?? "—"));
  setText("m-lambda", String(s.lambda_functions ?? "—"));

  $("tbl-ec2").innerHTML = (d.instances || [])
    .map(
      (row) => `
    <tr>
      <td>${row.Tags?.Name || "—"}</td>
      <td class="mono">${row.InstanceId}</td>
      <td>${row.InstanceType}</td>
      <td><span class="${stateClass(row.State)}">${row.State}</span></td>
      <td>${row.AvailabilityZone || "—"}</td>
    </tr>`
    )
    .join("");

  $("tbl-alarms").innerHTML = (d.alarms || [])
    .map(
      (row) => `
    <tr>
      <td>${row.AlarmName}</td>
      <td><span class="${stateClass(row.StateValue)}">${row.StateValue}</span></td>
      <td class="muted">${row.Namespace}/${row.MetricName}</td>
    </tr>`
    )
    .join("");

  $("tbl-alb").innerHTML = (d.load_balancers || [])
    .map(
      (row) => `
    <tr>
      <td class="mono">${row.DNSName}</td>
      <td>${row.Type}</td>
      <td>${row.Scheme}</td>
      <td><span class="${stateClass(row.State)}">${row.State}</span></td>
    </tr>`
    )
    .join("");

  $("tbl-lambda").innerHTML = (d.functions || [])
    .map(
      (row) => `
    <tr>
      <td>${row.FunctionName}</td>
      <td>${row.Runtime || "—"}</td>
      <td>${row.MemorySize} MB</td>
    </tr>`
    )
    .join("");

  $("tbl-s3").innerHTML = (d.buckets || [])
    .map(
      (row) => `
    <tr>
      <td class="mono">${row.Name}</td>
      <td class="muted">${(row.CreationDate || "").slice(0, 10)}</td>
    </tr>`
    )
    .join("");
}

async function loadDashboard() {
  showErr("");
  setText("status", "Loading…");
  try {
    const r = await fetch("/api/dashboard");
    const data = await r.json();
    if (!r.ok) throw new Error(data.error || `HTTP ${r.status}`);
    render(data);
    setText("status", "Updated " + new Date().toLocaleTimeString());
  } catch (e) {
    setText("status", "");
    showErr(e.message || String(e));
  }
}

document.addEventListener("DOMContentLoaded", () => {
  $("btn-refresh")?.addEventListener("click", loadDashboard);
  loadDashboard();
});
