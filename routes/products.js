var express = require("express");
var path = require("path");
const { json } = require("express");
var es = require("event-stream");
var router = express.Router();

/* GET home page. */
router.get("/", function (req, res, next) {
  res.render("index", { title: "Express" });
});

router.post("/", function (req, res, next) {
  const name = req.body.name;
  const count = req.body.count;
  console.log(count);
  var spawn = require("child_process").spawn;
  var process = spawn("python3", [
    path.join(__dirname, "../scripts/newegg.py"),
    name,
    count,
  ]);
  console.log("Process created");
  allData = "";
  process.stdout.on("readable", function () {
    while ((data = process.stdout.read())) {
      allData += data;
    }
  });
  process.stderr.on("data", (data) => {
    console.log(`error:${data}`);
  });
  process.on("close", function (code) {
    if (code == 0) {
      res.send({ data: "[" + allData + "]" });
    }
  });
});

module.exports = router;
