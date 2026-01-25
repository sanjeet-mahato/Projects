// Fetch dashboard data from backend
fetch("/dashboard-data")
  .then(res => res.json())
  .then(resp => {
    if(resp.status !== "success") return;

    const data = resp.data.detailed_data;
    const months = Object.keys(data);
    const debitValues = months.map(m => data[m].debit.total || 0);
    const creditValues = months.map(m => data[m].credit.total || 0);

    // KPIs
    const totalDebit = debitValues.reduce((a,b)=>a+b,0);
    const totalCredit = creditValues.reduce((a,b)=>a+b,0);
    const netBalance = totalCredit - totalDebit;
    const avgExpense = totalDebit / months.length;

    document.getElementById("totalDebit").textContent = `₹${totalDebit.toLocaleString()}`;
    document.getElementById("totalCredit").textContent = `₹${totalCredit.toLocaleString()}`;
    document.getElementById("netBalance").textContent = `₹${netBalance.toLocaleString()}`;
    document.getElementById("avgExpense").textContent = `₹${avgExpense.toFixed(0)}`;

    // Monthly Bar Chart
    new Chart(document.getElementById("monthlyBar"), {
      type: "bar",
      data: {
        labels: months,
        datasets: [
          {label: "Debit", data: debitValues, backgroundColor: "rgba(255,99,132,0.6)"},
          {label: "Credit", data: creditValues, backgroundColor: "rgba(54,162,235,0.6)"}
        ]
      },
      options: {responsive:true, scales:{y:{beginAtZero:true}}}
    });

    // Expense Line Chart
    const categories = new Set();
    months.forEach(m => {
      Object.keys(data[m].debit).forEach(k => { if(k !== "total") categories.add(k); });
    });

    const datasets = Array.from(categories).map((cat,i)=>{
      return {
        label: cat,
        data: months.map(m => data[m].debit[cat]?.total || 0),
        borderColor: ["#FF6384","#36A2EB","#FFCE56","#4BC0C0"][i%4],
        fill:false,
        tension:0.3
      };
    });

    new Chart(document.getElementById("expenseLine"), {
      type: "line",
      data: {labels: months, datasets: datasets},
      options: {responsive:true, scales:{y:{beginAtZero:true}}}
    });

    // Top Expenses List
    const topExpenses = [];
    months.forEach(m=>{
      Object.keys(data[m].debit).forEach(cat=>{
        if(cat==="total") return;
        const catData = data[m].debit[cat];
        Object.keys(catData.transactions).forEach(sub=>{
          topExpenses.push({
            date: m,
            category: cat,
            subcategory: sub,
            amount: catData.transactions[sub]
          });
        });
      });
    });

    topExpenses.sort((a,b)=>b.amount-a.amount);
    const listEl = document.getElementById("topExpenseList");
    topExpenses.slice(0,10).forEach(e=>{
      const li = document.createElement("li");
      li.textContent = `${e.date} — ${e.category} — ${e.subcategory} — ₹${e.amount.toLocaleString()}`;
      listEl.appendChild(li);
    });

    // Expense Pie Chart
    const pieData = {};
    topExpenses.forEach(e=> pieData[e.category] = (pieData[e.category]||0)+e.amount);
    new Chart(document.getElementById("expensePie"), {
      type:"pie",
      data:{labels:Object.keys(pieData), datasets:[{data:Object.values(pieData), backgroundColor:["#FF6384","#36A2EB","#FFCE56","#4BC0C0"]}]}
    });

    // Income Pie Chart (use credit categories)
    const incomeData = {};
    months.forEach(m=>{
      Object.keys(data[m].credit).forEach(cat=>{
        if(cat==="total") return;
        incomeData[cat] = (incomeData[cat]||0)+data[m].credit[cat].total;
      });
    });
    new Chart(document.getElementById("incomePie"), {
      type:"pie",
      data:{labels:Object.keys(incomeData), datasets:[{data:Object.values(incomeData), backgroundColor:["#36A2EB","#FF6384","#FFCE56","#4BC0C0"]}]}
    });
  })
  .catch(err=>console.error("Failed to fetch dashboard data:", err));
