(async () => {
  try {
    // Fetch emissions summary data from backend API
    const response = await fetch("/api/analysis/emissions/summary");
    
    if (!response.ok) {
      console.warn("Failed to fetch emissions summary data");
      return;
    }
    
    const data = await response.json();
    
    // Extract values with fallbacks
    const total = Number(data.total_tco2e ?? 0);
    const records = Number(data.records ?? 0);
    const standard = String(data.standard ?? "ISO");
    
    // Format numbers for display
    const formatter = new Intl.NumberFormat("en-US", { 
      maximumFractionDigits: 3,
      minimumFractionDigits: 0
    });
    
    // Update DOM elements
    const elTotal = document.getElementById("kpiTotal");
    const elRecords = document.getElementById("kpiRecords");
    const elStandard = document.getElementById("kpiStandard");
    
    if (elTotal) {
      elTotal.textContent = formatter.format(total);
    }
    
    if (elRecords) {
      elRecords.textContent = formatter.format(records);
    }
    
    if (elStandard) {
      elStandard.textContent = standard;
    }
    
  } catch (error) {
    console.error("Error loading emissions summary:", error);
    
    // Show fallback values on error
    const elTotal = document.getElementById("kpiTotal");
    const elRecords = document.getElementById("kpiRecords");
    
    if (elTotal) elTotal.textContent = "0";
    if (elRecords) elRecords.textContent = "0";
  }
})();