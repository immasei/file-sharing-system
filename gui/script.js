const windowEl = document.querySelector(".window");
const content = document.querySelector(".window-content");
const sidebarUL = document.querySelector(".window-sidebar ul");
const maximize = document.querySelector("#maximize");
const close = document.querySelector("#close");
const darkMode = document.querySelector("#dark-mode");

darkMode.addEventListener("click", function () {
  document.documentElement.classList.toggle("dark");
});

close.addEventListener("click", () => (windowEl.style.display = "none"));
maximize.addEventListener("click", () => {
  windowEl.classList.toggle("maximized");
});

const addSidebarItems = function (items) {
  let html = "";
  items.forEach(item => {
    html += `
      <li class="sidebar-item ${item[0] === "home" ? "active" : ""}">
        <i class="fas fa-${item[0]} sidebar-item-icon"></i>
        <span class="sidebarUL-item-text">${item[1]}</span>
      </li>
    `;
  });

  sidebarUL.insertAdjacentHTML("beforeend", html);
};

const addFolders = function (folders) {
  let html = "";
  folders.forEach(folder => {
    html += `
      <div class="content-item folder">
        <i class="fas fa-folder icon"></i>
        <span class="text">${folder}</span>
      </div>
    `;
  });

  content.insertAdjacentHTML("beforeend", html);
};

const addFiles = function (files) {
  let html = "";
  files.forEach(file => {
    html += `
      <div class="content-item file">
        <i class="fas fa-file${file[0]} icon"></i>
        <span class="text">${file[1]}</span>
      </div>    
    `;
  });

  content.insertAdjacentHTML("beforeend", html);
};

const sidebarItems = [
  ["history", "Recent"],
  ["home", "Home"],
  ["download", "Downloads"],
  ["image", "Pictures"],
  ["music", "Musics"],
  ["video", "Movies"],
  ["book", "Documents"],
  ["trash", "Trash"],
  ["network-wired", "Network"],
];

const folders = [
  "Desktop",
  "Downloads",
  "Musics",
  "Pictures",
  "Movies",
  "Templates",
  "Public",
];
const files = [
  ["-word", "word.docx"],
  ["-code", "script.js"],
  ["-pdf", "homework.pdf"],
  ["-image", "logo.jpg"],
  ["", "data.bin"],
];

addSidebarItems(sidebarItems);
addFolders(folders);
addFiles(files);