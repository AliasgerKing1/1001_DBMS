const express = require("express");
const app = express();
const routes = require("./config/routes");
const cors = require("cors");

app.use(express.json());
app.use(express.urlencoded({extended : true}));
app.use(express.static(__dirname + "/assets"));
app.use(cors());


app.use(routes);

const port = process.env.PORT || 4015;
app.listen(port, ()=> {
    console.log(`Server Running on port ${port}`);
})