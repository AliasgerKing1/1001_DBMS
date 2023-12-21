const routes = require("express").Router();

routes.use("/api/dbms", require("../controller/DbmsController"));

module.exports = routes;