// 바로GO — 모바일 내비게이션 토글 + 드롭다운 접근성
(function () {
  "use strict";
  document.addEventListener("DOMContentLoaded", function () {
    var toggle = document.querySelector(".nav-toggle");
    var menu = document.querySelector(".nav-menu");
    if (toggle && menu) {
      toggle.addEventListener("click", function () {
        var open = menu.classList.toggle("open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
      });
    }
    // 모바일: 드롭다운이 있는 상위 메뉴를 탭하면 펼침
    document.querySelectorAll(".nav-item").forEach(function (item) {
      var hasDrop = item.querySelector(".dropdown");
      var link = item.querySelector("a");
      if (!hasDrop || !link) return;
      link.addEventListener("click", function (e) {
        if (window.matchMedia("(max-width: 768px)").matches) {
          if (link.getAttribute("href") === "#" || !item.classList.contains("open")) {
            e.preventDefault();
            item.classList.toggle("open");
          }
        }
      });
    });
  });
})();
