// 導入共用 header
fetch("include/header.html")
  .then(res => res.text())
  .then(data => document.getElementById("header-placeholder").innerHTML = data);

// 代辦任務新增與刪除
const taskInput = document.getElementById("taskInput");
const addTaskBtn = document.getElementById("addTaskBtn");
const taskList = document.getElementById("taskList");
const generatePlanBtn = document.getElementById("generatePlanBtn");
const suggestionCards = document.getElementById("suggestionCards");

if (addTaskBtn) {
  addTaskBtn.addEventListener("click", () => {
    const taskName = taskInput.value.trim();
    if (!taskName) return;
    const li = document.createElement("li");
    li.className = "list-group-item d-flex justify-content-between align-items-center";
    li.innerHTML = `${taskName} <button class="btn btn-sm btn-danger">刪除</button>`;
    li.querySelector("button").addEventListener("click", () => li.remove());
    taskList.appendChild(li);
    taskInput.value = "";
  });
}

// 模擬 AI 建議行程
if (generatePlanBtn) {
  generatePlanBtn.addEventListener("click", () => {
    const tasks = ["洗衣服 (宿舍)", "做資料分析簡報 (圖書館B1興閱坊)"];
    suggestionCards.innerHTML = "";
    tasks.forEach((task, i) => {
      const card = document.createElement("div");
      card.className = "col-12 col-md-6 mb-3";
      card.innerHTML = `
        <div class="card shadow-sm border-0" style="border-left:5px solid #316a99;">
          <div class="card-body">
            <h5>${task}</h5>
            <p><strong>建議時段：</strong>${i===0 ? "10:30-11:00" : "15:30-17:00"}<br>
               <strong>地點：</strong>${i===0 ? "宿舍" : "圖書館 B1 興閱坊"}<br>
               <strong>優先順序：</strong>${i===0 ? "高" : "中"}</p>
          </div>
        </div>`;
      suggestionCards.appendChild(card);
    });
  });
}
