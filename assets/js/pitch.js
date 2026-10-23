/* Proposal page: scales the live site previews to fit their device frames. */
(function () {
  "use strict";
  function fit() {
    document.querySelectorAll("[data-scale-frame]").forEach(function (frame) {
      var screen = frame.querySelector(".device-screen");
      var iframe = frame.querySelector("iframe");
      var width = Number(frame.getAttribute("data-frame-width"));
      var scale = screen.clientWidth / width;
      iframe.style.width = width + "px";
      iframe.style.height = (screen.clientHeight / scale) + "px";
      iframe.style.transform = "scale(" + scale + ")";
    });
  }
  window.addEventListener("load", fit);
  window.addEventListener("resize", fit);
  document.addEventListener("DOMContentLoaded", fit);
})();
