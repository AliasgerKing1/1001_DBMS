const routes = require("express").Router();
const sha1 = require("sha1")
const Dbms_table = require("../models/Dbms_table");
const jwt = require("jsonwebtoken")

routes.post("/",  async(req,res) => {
    body = req.body
    body?.property_lst?.map((property) => (
        property.count = parseInt(property.count)
    ))
    let result = await Dbms_table.create(body);
    res.send({status : 200, success : true, data : result})
})

routes.get("/", async (req,res)=> {
    if(req.headers.token) {
        let token = req.headers.token;
        let obj = jwt.decode(token, "Aliasger web")
        let result = await Dbms_table.find({_id : obj._id})
        res.send(result)
    }
})


routes.put('/', async (req, res) => {
    try {
      let result = await Dbms_table.find({ table_name: req.body.table_name.trim() });
  
      if (result?.length > 0) {
        const reqBodyKeys = Object.keys(req.body).filter((key) => key !== 'table_name');
  
        if (reqBodyKeys?.length !== result[0]?.property_lst?.length) {
          return res.status(400).json({ status: 400, success: false, msg: `Number of properties is incorrect, Expected ${result[0]?.property_lst?.length} properties` });
        }
  
        let status = 200;
        let success = true;
        let msg = 'Data insert Successfully';
  
        // Extract values excluding table_name
        const actualDataObject = Object.fromEntries(Object.entries(req.body).filter(([key]) => key !== 'table_name'));
  
        // Additional checks for data type and max character length
        for (const [key, value] of Object.entries(actualDataObject)) {
          const propIndex = parseInt(key.replace('prop', ''), 10);
          const prop = result[0]?.property_lst[propIndex];
  
          if (typeof value !== prop.type) {
            status = 400;
            success = false;
            msg = `${key} has an unexpected type. Expected: ${prop.type}, Actual: ${typeof value}`;
            break;
          } else if (
            (typeof value === 'string' && value.length > prop.count) ||
            (typeof value === 'number' && value.toString().length > prop.count)
          ) {
            status = 400;
            success = false;
            msg = `${key} exceeds the maximum allowed length. Maximum: ${prop.count}, Actual: ${value.toString().length}`;
            break;
          }
        }
  
        // If there are no errors, append the object to the actual-data array
        if (success) {
          await Dbms_table.updateMany(
            { table_name: req.body.table_name },
            { $push: { 'actual_data': actualDataObject } }
          );
          insetedData = actualDataObject;
          propertiesArray = result[0]?.property_lst
        }
  
        return res.status(status).json({ status, success, msg, insetedData, propertiesArray});
      } else {
        res.status(400).json({ status: 400, success: false, msg: `No item created with name ${req.body.table_name.trim()}` });
      }
    } catch (error) {
      console.error(error);
      return res.status(500).json({ status: 500, success: false, msg: 'Internal Server Error' });
    }
  });
  
  
  
module.exports = routes;