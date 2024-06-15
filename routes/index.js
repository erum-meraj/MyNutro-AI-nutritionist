const express = require("express");
const router = express.Router();

router.get("/", (req, res, next) => {
  res.render("index", { title: "Home" });
});

router.get("/diet-plan", (req, res, next) => {
  res.render("diet_plan", { title: "Home" });
});

module.exports = router;
