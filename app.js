const createError = require("http-errors");
const express = require("express");
const path = require("path");
const cookieParser = require("cookie-parser");
const logger = require("morgan");
const session = require("express-session");

const indexRouter = require("./routes/index");
// If you uncomment this line, ensure the corresponding route file exists
// const formRouter = require("./routes/form");

const app = express();

// Session setup
app.use(
  session({
    secret: "websession",
    resave: true,
    saveUninitialized: true,
  })
);

// View engine setup
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));

// Routes
app.use("/", indexRouter);
// Uncomment this if the form route exists
// app.use("/form", formRouter);
app.get("/", (req, res) => {
  // Fetch data from the database
  res.render("index");
});

app.get("/diet_plan", (req, res) => {
  // Fetch data from the database
  res.render("diet_plan");
});

app.get("/about", (req, res) => {
  // Fetch data from the database
  res.render("about");
});

app.get("/contact", (req, res) => {
  // Fetch data from the database
  res.render("contact");
});

// Catch 404 and forward to error handler
app.use((req, res, next) => {
  next(createError(404));
});

// Error handler
app.use((err, req, res, next) => {
  // Set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get("env") === "development" ? err : {};

  // Render the error page
  res.status(err.status || 500);
  res.render("error");
});

module.exports = app;

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
