const express = require("express");
const router = express.Router();
const axios = require("axios");

router.get("/", (req, res, next) => {
  res.render("index", { title: "Home" });
});

router.get("/diet-plan", (req, res, next) => {
  const result = "";
  res.render("diet_plan", { title: "Diet Plan", result: result });
});

router.post("/generate", async (req, res, next) => {
  const problem = req.body.problems;
  const diettype = req.body.diettype;
  const country = req.body.country;

  try {
    const response = await axios.post("http://localhost:5000/predict", {
      problems: problem,
      diettype: diettype,
      country: country,
    });

    const result = response.data; // Assuming Flask returns the entire result object

    // Render index.ejs with the result
    res.render("diet_plan", { title: "Diet Plan", result: result });
  } catch (error) {
    console.error("Error calling Flask API:", error);
    res.status(500).json({ error: "Failed to call Flask API" });
  }
});

module.exports = router;
