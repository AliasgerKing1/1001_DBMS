require("../config/database")
const mongoose = require("mongoose");

const Dbms_table = mongoose.Schema({
    table_name : String,
    property_lst : Array,
    actual_data : Array
})
module.exports = mongoose.model("dbms-table", Dbms_table);