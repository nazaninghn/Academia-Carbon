// Analysis Emissions JavaScript - Professional Implementation

(() => {
  const state = {
    standard: "ghg",
    dateFrom: null,
    dateTo: null,
    facility: "all",
    selected: {
      scopes: new Set(),
      // "1", "2", "3"
      categories: new Set(),   // e.g., "stationary"
      sources: new Set(),      // e.g., "coal-industrial"
    },
    page: 1,
    rowsPerPage: 10,
    sortBy: "value_desc",
    search: "",
    treeData: null,
    chart: null,
    lastPayload: null,
  };

  const el = (id) => document.getElementById(id);

  // Initialize page when DOM is ready
  document.addEventListener('DOMContentLoaded', function() {
    initializePage();
  });

  function initializePage() {
    // Set default date range (last 12 months)
    const today = new Date();
    const lastYear = new Date(today.getFullYear() - 1, today.getMonth(), today.getDate());
    
    el('dateFrom').value = lastYear.toISOString().split('T')[0];
    el('dateTo').value = today.toISOString().split('T')[0];
    
    state.dateFrom = lastYear.toISOString().split('T')[0];
    state.dateTo = today.toISOString().split('T')[0];
    
    setupEventListeners();
    fetchAndRender();
  }

  function setupEventListeners() {
    // Standard tabs
    const tabs = document.querySelectorAll(".tab");
    tabs.forEach((btn) => {
      btn.addEventListener("click", () => {
        tabs.forEach((b) => b.classList.remove("tab-active"));
        btn.classList.add("tab-active");
        state.standard = btn.dataset.standard;
        fetchAndRender();
      });
    });

    el("applyFilters").addEventListener("click", () => {
      state.dateFrom = el("dateFrom").value || null;
      state.dateTo = el("dateTo").value || null;
      state.facility = el("facility").value || "all";
      state.page = 1;
      fetchAndRender();
    });

    el("sortBy").addEventListener("change", () => {
      state.sortBy = el("sortBy").value;
      state.page = 1;
      renderTable(state.lastPayload);
    });

    el("rowsPerPage").addEventListener("change", () => {
      state.rowsPerPage = parseInt(el("rowsPerPage").value, 10);
      state.page = 1;
      renderTable(state.lastPayload);
    });

    el("prevPage").addEventListener("click", () => {
      if (state.page > 1) {
        state.page -= 1;
        renderTable(state.lastPayload);
      }
    });

    el("nextPage").addEventListener("click", () => {
      state.page += 1;
      renderTable(state.lastPayload);
    });

    el("treeSearch").addEventListener("input", (e) => {
      state.search = e.target.value.trim().toLowerCase();
      renderTree(state.treeData);
    });

    el("clearSearch").addEventListener("click", () => {
      state.search = "";
      el("treeSearch").value = "";
      renderTree(state.treeData);
    });

    el("clearAll").addEventListener("click", () => {
      state.selected.scopes.clear();
      state.selected.categories.clear();
      state.selected.sources.clear();
      state.page = 1;
      renderTree(state.treeData);
      fetchAndRender();
    });

    // Export button
    el("exportTable").addEventListener("click", () => {
      exportToExcel();
    });
  }

  function buildQuery() {
    const params = new URLSearchParams();
    if (state.standard) params.set("standard", state.standard);
    if (state.dateFrom) params.set("from", state.dateFrom);
    if (state.dateTo) params.set("to", state.dateTo);
    if (state.facility) params.set("facility", state.facility);

    if (state.selected.scopes.size) params.set("scopes", Array.from(state.selected.scopes).join(","));
    if (state.selected.categories.size) params.set("categories", Array.from(state.selected.categories).join(","));
    if (state.selected.sources.size) params.set("sources", Array.from(state.selected.sources).join(","));

    return params.toString();
  }

  async function fetchAndRender() {
    const url = `/en/api/emissions/data/?${buildQuery()}`;
    try {
      const res = await fetch(url);
      if (!res.ok) {
        console.error("API error", res.status);
        showToast('Failed to load emissions data', 'error');
        return;
      }
      const payload = await res.json();
      state.lastPayload = payload;

      // Cache tree data once
      if (!state.treeData) {
        state.treeData = payload.tree || buildDefaultTree();
        renderTree(state.treeData);
      }

      renderChart(payload);
      renderBreakdown(payload);
      renderTable(payload);
    } catch (error) {
      console.error('Error loading emissions data:', error);
      showToast('Failed to load emissions data', 'error');
    }
  }

  function buildDefaultTree() {
    // Build default tree structure based on emission factors
    return {
      scopes: [
        {
          id: "1",
          name: "Scope 1",
          _collapsed: false,
          categories: [
            {
              key: "stationary",
              name: "Stationary Combustion",
              _collapsed: false,
              sources: [
                { key: "coal-industrial", name: "Coal (industrial)" },
                { key: "natural-gas", name: "Natural Gas" },
                { key: "diesel-oil", name: "Gas/Diesel Oil" },
                { key: "lpg", name: "LPG" },
                { key: "propane", name: "Propane" },
                { key: "motor-gasoline", name: "Motor Gasoline" }
              ]
            },
            {
              key: "mobile",
              name: "Mobile Combustion", 
              _collapsed: false,
              sources: [
                { key: "off-road-gasoline", name: "Off-Road Gasoline" },
                { key: "off-road-diesel", name: "Off-Road Diesel" },
                { key: "on-road-diesel", name: "On-Road Diesel" },
                { key: "car-gasoline", name: "Car - Gasoline" },
                { key: "car-diesel", name: "Car - Diesel" }
              ]
            },
            {
              key: "fugitive",
              name: "Fugitive Emissions",
              _collapsed: false,
              sources: [
                { key: "r432a", name: "R432A" },
                { key: "r410a", name: "R410A" },
                { key: "r134a", name: "R134a" }
              ]
            }
          ]
        },
        {
          id: "2",
          name: "Scope 2",
          _collapsed: false,
          categories: [
            {
              key: "electricity",
              name: "Electricity",
              _collapsed: false,
              sources: [
                { key: "grid-electricity", name: "Grid Electricity" },
                { key: "renewable-energy", name: "Renewable Energy" }
              ]
            },
            {
              key: "heat-steam",
              name: "Heat and Steam",
              _collapsed: false,
              sources: [
                { key: "district-heating", name: "District Heating" },
                { key: "steam", name: "Steam" }
              ]
            }
          ]
        },
        {
          id: "3", 
          name: "Scope 3",
          _collapsed: false,
          categories: [
            {
              key: "purchased-goods",
              name: "Purchased Goods",
              _collapsed: false,
              sources: [
                { key: "paper", name: "Paper" },
                { key: "plastic", name: "Plastic" },
                { key: "metal", name: "Metal" },
                { key: "chemical", name: "Chemical" },
                { key: "wood", name: "Wood" }
              ]
            },
            {
              key: "business-travel",
              name: "Business Travel",
              _collapsed: false,
              sources: [
                { key: "flight", name: "Flight" },
                { key: "hotel", name: "Hotel" },
                { key: "car-rental", name: "Car Rental" },
                { key: "train", name: "Train" }
              ]
            },
            {
              key: "waste",
              name: "Waste",
              _collapsed: false,
              sources: [
                { key: "waste", name: "Waste" },
                { key: "recycling", name: "Recycling" },
                { key: "landfill", name: "Landfill" }
              ]
            }
          ]
        }
      ]
    };
  }

  function renderTree(tree) {
    const root = el("scopeTree");
    root.innerHTML = "";

    (tree.scopes || []).forEach((scope) => {
      const scopeNode = document.createElement("div");
      scopeNode.className = "tree-scope";

      const scopeHeader = document.createElement("div");
      scopeHeader.className = "tree-row";

      const left = document.createElement("div");
      left.className = "tree-left";

      const toggle = document.createElement("span");
      toggle.className = "tree-toggle";
      toggle.textContent = scope._collapsed ? "+" : "−";
      toggle.addEventListener("click", () => {
        scope._collapsed = !scope._collapsed;
        renderTree(tree);
      });

      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.checked = state.selected.scopes.has(scope.id);
      checkbox.addEventListener("change", () => {
        if (checkbox.checked) state.selected.scopes.add(scope.id);
        else state.selected.scopes.delete(scope.id);
        state.page = 1;
        fetchAndRender();
      });

      const label = document.createElement("div");
      label.className = "tree-label";
      label.textContent = scope.name;

      left.appendChild(toggle);
      left.appendChild(checkbox);
      left.appendChild(label);

      const actions = document.createElement("div");
      actions.className = "tree-actions";

      const badge = document.createElement("span");
      badge.className = "badge";
      badge.textContent = "All";

      const clear = document.createElement("button");
      clear.className = "link";
      clear.textContent = "Clear";
      clear.addEventListener("click", () => {
        state.selected.scopes.delete(scope.id);
        // clear all categories and sources under this scope
        (scope.categories || []).forEach((c) => {
          state.selected.categories.delete(c.key);
          (c.sources || []).forEach((s) => state.selected.sources.delete(s.key));
        });
        state.page = 1;
        renderTree(tree);
        fetchAndRender();
      });

      actions.appendChild(badge);
      actions.appendChild(clear);

      scopeHeader.appendChild(left);
      scopeHeader.appendChild(actions);

      scopeNode.appendChild(scopeHeader);

      if (!scope._collapsed) {
        const children = document.createElement("div");
        children.className = "tree-children";

        (scope.categories || []).forEach((cat) => {
          // Search filter
          const catText = (cat.name || "").toLowerCase();
          const matchCat = !state.search || catText.includes(state.search);

          const catWrap = document.createElement("div");
          catWrap.className = "tree-item";

          const catRow = document.createElement("div");
          catRow.className = "tree-row";

          const catLeft = document.createElement("div");
          catLeft.className = "tree-left";

          const catToggle = document.createElement("span");
          catToggle.className = "tree-toggle";
          catToggle.textContent = cat._collapsed ? "+" : "−";
          catToggle.addEventListener("click", () => {
            cat._collapsed = !cat._collapsed;
            renderTree(tree);
          });

          const catCb = document.createElement("input");
          catCb.type = "checkbox";
          catCb.checked = state.selected.categories.has(cat.key);
          catCb.addEventListener("change", () => {
            if (catCb.checked) state.selected.categories.add(cat.key);
            else state.selected.categories.delete(cat.key);
            state.page = 1;
            fetchAndRender();
          });

          const catLabel = document.createElement("div");
          catLabel.className = "tree-label";
          catLabel.textContent = cat.name;

          catLeft.appendChild(catToggle);
          catLeft.appendChild(catCb);
          catLeft.appendChild(catLabel);

          const catRight = document.createElement("div");
          catRight.className = "tree-actions";
          const ok = document.createElement("span");
          ok.className = "badge";
          ok.textContent = "✓";
          catRight.appendChild(ok);

          catRow.appendChild(catLeft);
          catRow.appendChild(catRight);
          catWrap.appendChild(catRow);

          if (!cat._collapsed) {
            const srcList = document.createElement("div");
            srcList.className = "tree-children";

            (cat.sources || []).forEach((src) => {
              const srcText = (src.name || "").toLowerCase();
              const matchSrc = !state.search || srcText.includes(state.search);
              if (!state.search || matchCat || matchSrc) {
                const sRow = document.createElement("div");
                sRow.className = "tree-row";

                const sLeft = document.createElement("div");
                sLeft.className = "tree-left";

                const sCb = document.createElement("input");
                sCb.type = "checkbox";
                sCb.checked = state.selected.sources.has(src.key);
                sCb.addEventListener("change", () => {
                  if (sCb.checked) state.selected.sources.add(src.key);
                  else state.selected.sources.delete(src.key);
                  state.page = 1;
                  fetchAndRender();
                });

                const sLabel = document.createElement("div");
                sLabel.className = "tree-label";
                sLabel.textContent = src.name;

                sLeft.appendChild(document.createElement("span")).className = "tree-toggle";
                sLeft.appendChild(sCb);
                sLeft.appendChild(sLabel);

                const dot = document.createElement("span");
                dot.className = "badge";
                dot.textContent = "•";

                sRow.appendChild(sLeft);
                sRow.appendChild(dot);
                srcList.appendChild(sRow);
              }
            });

            catWrap.appendChild(srcList);
          }

          // Hide category block if search doesn't match anything
          if (!state.search || matchCat) {
            children.appendChild(catWrap);
          } else {
            // If category doesn't match, it might still have matching sources (handled above).
            children.appendChild(catWrap);
          }
        });

        scopeNode.appendChild(children);
      }

      root.appendChild(scopeNode);
    });
  }

  function renderChart(payload) {
    const ctx = document.getElementById("scopeDonut");
    const labels = payload.scope_chart?.labels || ['Scope 1', 'Scope 2', 'Scope 3'];
    const values = payload.scope_chart?.values || [
      payload.scope1 || 0,
      payload.scope2 || 0, 
      payload.scope3 || 0
    ];

    // Update total
    const total = values.reduce((sum, val) => sum + val, 0);
    el("totalValue").textContent = `${(total / 1000).toFixed(2)} tCO₂e`;

    if (state.chart) {
      state.chart.data.labels = labels;
      state.chart.data.datasets[0].data = values;
      state.chart.update();
      return;
    }

    state.chart = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels,
        datasets: [{ 
          data: values,
          backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6'],
          borderWidth: 0
        }],
      },
      options: {
        responsive: true,
        cutout: "68%",
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (item) => {
                const value = (item.raw / 1000).toFixed(3);
                const percentage = total > 0 ? ((item.raw / total) * 100).toFixed(1) : 0;
                return `${item.label}: ${value} tCO₂e (${percentage}%)`;
              },
            },
          },
        },
      },
    });
  }

  function renderBreakdown(payload) {
    const list = el("breakdownList");
    list.innerHTML = "";

    const total = (payload.scope1 || 0) + (payload.scope2 || 0) + (payload.scope3 || 0);
    const breakdown = [
      { name: 'Scope 1', value: payload.scope1 || 0 },
      { name: 'Scope 2', value: payload.scope2 || 0 },
      { name: 'Scope 3', value: payload.scope3 || 0 }
    ].filter(item => item.value > 0);

    breakdown.forEach((row) => {
      const div = document.createElement("div");
      div.className = "summary-row";

      const name = document.createElement("div");
      name.className = "summary-name";
      name.textContent = row.name;

      const pct = document.createElement("div");
      pct.className = "summary-percent";
      const percentage = total > 0 ? ((row.value / total) * 100).toFixed(1) : 0;
      pct.textContent = `${percentage}%`;

      const val = document.createElement("div");
      val.className = "summary-value";
      val.textContent = (row.value / 1000).toFixed(3);

      div.appendChild(name);
      div.appendChild(pct);
      div.appendChild(val);
      list.appendChild(div);
    });
  }

  function sortRows(rows) {
    const sort = state.sortBy;
    const copy = [...rows];

    const cmp = {
      value_desc: (a, b) => (b.emissions || 0) - (a.emissions || 0),
      value_asc: (a, b) => (a.emissions || 0) - (b.emissions || 0),
      pct_desc: (a, b) => (b.percentage || 0) - (a.percentage || 0),
      pct_asc: (a, b) => (a.percentage || 0) - (b.percentage || 0),
      name_asc: (a, b) => (a.name || "").localeCompare(b.name || ""),
    }[sort];

    return copy.sort(cmp);
  }

  function renderTable(payload) {
    if (!payload) return;

    const body = el("sourcesTableBody");
    body.innerHTML = "";

    const sources = payload.sources || [];
    if (sources.length === 0) {
      body.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--muted); padding: 40px;">No emission sources found for the selected filters.</td></tr>';
      el("tableMeta").textContent = '0 rows';
      return;
    }

    const rows = sortRows(sources);
    const totalRows = rows.length;
    const total = rows.reduce((sum, source) => sum + (source.emissions || 0), 0);

    const start = (state.page - 1) * state.rowsPerPage;
    const end = start + state.rowsPerPage;
    const pageRows = rows.slice(start, end);

    // If page is out of range, reset
    if (state.page > 1 && pageRows.length === 0) {
      state.page = 1;
      return renderTable(payload);
    }

    const maxVal = rows.length ? (rows[0].emissions || 0) : 0.0;

    pageRows.forEach((r) => {
      const tr = document.createElement("tr");

      const tdName = document.createElement("td");
      tdName.className = "source-name";
      tdName.textContent = r.name || r.source_name || '';

      const tdScope = document.createElement("td");
      const scopeBadge = document.createElement("span");
      scopeBadge.className = `scope-badge scope${r.scope || 1}`;
      scopeBadge.textContent = `Scope ${r.scope || 1}`;
      tdScope.appendChild(scopeBadge);

      const tdVal = document.createElement("td");
      tdVal.className = "num emissions-value";
      const emissions = r.emissions || 0;
      tdVal.textContent = (emissions / 1000).toFixed(3);

      const tdPct = document.createElement("td");
      tdPct.className = "num";
      const percentage = total > 0 ? ((emissions / total) * 100).toFixed(1) : 0;
      tdPct.textContent = `${percentage}%`;

      const tdDist = document.createElement("td");
      const bar = document.createElement("div");
      bar.className = "dist-bar";

      const fill = document.createElement("div");
      fill.className = "dist-fill";

      const pctWidth = maxVal > 0 ? (emissions / maxVal) * 100 : 0;
      fill.style.width = `${Math.min(pctWidth, 100)}%`;

      bar.appendChild(fill);
      tdDist.appendChild(bar);

      tr.appendChild(tdName);
      tr.appendChild(tdScope);
      tr.appendChild(tdVal);
      tr.appendChild(tdPct);
      tr.appendChild(tdDist);

      body.appendChild(tr);
    });

    el("tableMeta").textContent = `${totalRows} rows • Page ${state.page}`;
    
    // Update pagination buttons
    const totalPages = Math.ceil(totalRows / state.rowsPerPage);
    el("prevPage").disabled = state.page === 1;
    el("nextPage").disabled = state.page >= totalPages;
  }

  function exportToExcel() {
    if (!state.lastPayload || !state.lastPayload.sources) {
      showToast('No data to export', 'error');
      return;
    }

    const url = `/en/api/emissions/export/?${buildQuery()}`;
    window.open(url, '_blank');
    showToast('Export started...', 'success');
  }

  function showToast(message, type = 'success') {
    const colors = {
      'success': '#10B981',
      'error': '#EF4444',
      'info': '#3B82F6'
    };
    
    const toast = document.createElement('div');
    toast.style.cssText = `
      position: fixed; 
      top: 20px; 
      right: 20px; 
      background: ${colors[type]}; 
      color: white; 
      padding: 15px 25px; 
      border-radius: 10px; 
      z-index: 10000; 
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      font-weight: 500;
    `;
    toast.innerHTML = `<i class="fas fa-info-circle"></i> ${message}`;
    document.body.appendChild(toast);
    
    setTimeout(() => {
      toast.remove();
    }, 3000);
  }

})();